from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, StreamInfoForm, StreamKeyForm
from app.models import User
from app import csrf
from app import db
from app import ph
import app.keygen as keygen
import bleach
import xml.etree.ElementTree as ET
import requests

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('main_bp.home'))

@main_bp.route('/home')
def home():
    return render_template('home.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and ph.verify(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main_bp.profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.login'))

@main_bp.route('/profile')
@login_required
def profile():
    stream_info_form = StreamInfoForm()
    stream_info_form.name.data = current_user.stream_name
    stream_key_form = StreamKeyForm()
    stream_key_form.key.data = current_user.stream_key

    return render_template('profile.html', stream_info_form=stream_info_form, stream_key_form=stream_key_form)

@main_bp.route('/api/stream', methods=['GET', 'PUT'])
@login_required
def stream_name():
    if request.method == 'PUT':
        stream_data = request.get_json()
        name = stream_data.get('name')
        if name:
            current_user.stream_name = bleach.clean(name)
            db.session.commit()

    return jsonify({
            'status': 'success',
            'data': {
                'name': current_user.stream_name,
            },
        })
    
@main_bp.route('/api/stream/key', methods=['GET', 'DELETE'])
@login_required
def stream_key():
    if request.method == 'DELETE':
        key = keygen.generate_key()
        current_user.stream_key = key
        db.session.commit()

    return jsonify({
            'status': 'success',
            'data': {
                'key': current_user.stream_key,
            },
        })

@main_bp.route('/api/keys/<key>')
def stream_key_validate(key):
    user = User.query.filter_by(stream_key=key).first()
    if user:
        return jsonify({
                'status': 'success',
                'data': {
                    'state': 'valid',
                    'user_id': user.id,
                },
            })
    else:
        return jsonify({
                'status': 'success',
                'data': {
                    'state': 'invalid',
                },
            }), 401
    
@main_bp.route('/api/streams')
def streams():
    response = requests.get('http://nginx:8080/stat')
    if response.status_code == 200:
        streams = []
        root = ET.fromstring(response.text)
        for stream_key_el in root.findall(".//server/application/live/stream/name"):
            user = User.query.filter_by(stream_key=stream_key_el.text).first()
            if user:
                streams.append({"name": user.stream_name})

        return jsonify({
                'status': 'success',
                'data': {
                    'streams': streams,
                },
            })
    
@main_bp.route('/api/streams/<int:stream_id>/name.txt')
def stream(stream_id):
    user = User.query.filter_by(id=stream_id).first()
    if user:
        return user.stream_name
    else:
        return "Stream name not found", 404