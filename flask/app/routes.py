from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegisterForm, StreamInfoForm, StreamKeyForm, AvatarForm
from app.models import User
from app import csrf
from app import db
from app import ph
from jinja2 import Template
import app.keygen as keygen
import bleach
import xml.etree.ElementTree as ET
import requests
import os
import time

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('main_bp.home'))

@main_bp.route('/home')
def home():
    users = get_streaming_users()
    return render_template('home.html', users=users)

@main_bp.route("/rec")
def recordings():
    recordings = []
    directory_path = "/recordings"
    for f in os.scandir(directory_path):
        if f.is_file():
            file_name = f.name
            id = os.path.splitext(file_name)[0]
            user = User.query.filter_by(id=id).first()
            if user:
                ctime = time.ctime(f.stat().st_ctime)
                recordings.append({
                        'file_name': file_name,
                        'username': user.username,
                        'time': ctime,
                    })

    return render_template('recordings.html', recordings=recordings)

@main_bp.route("/theme", methods=['PUT'])
def theme():
    theme_data = request.get_json()
    theme = theme_data.get('theme')
    if theme in ['light', 'dark']:
        session['theme'] = theme
        return jsonify({
            'status': 'success',
            'data': {
                'theme': session['theme'],
            },
        })

    return jsonify({
            'status': 'error',
            'data': {
                'theme': session['theme'],
            },
        }), 400

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        username = bleach.clean(form.username.data)
        user = User.query.filter_by(username=username).first()
        if user:
            try:
                ph.verify(user.password, form.password.data)
                login_user(user)
                return redirect(url_for('main_bp.profile'))
            except Exception:
                flash('Login Unsuccessful. Please check username and password', 'danger')    
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.profile'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = bleach.clean(form.username.data)
        if User.query.filter_by(username=username).first():
            flash('User already exists', 'danger')
        else:
            password = ph.hash(form.password.data)
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main_bp.profile'))
    return render_template('register.html', form=form)

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
    avatar_form = AvatarForm()

    return render_template('profile.html', stream_info_form=stream_info_form, stream_key_form=stream_key_form, avatar_form=avatar_form)

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    form = AvatarForm()
    if form.validate_on_submit():
        f = form.avatar.data
        f.save(os.path.join(current_app.static_folder, 'avatar', str(current_user.id)))
        return jsonify({
            'status': 'success',
            'data': None,
        })

    return jsonify({
            'status': 'error',
            'data': None,
        })

@main_bp.route('/scenes')
@login_required
def scenes():
    scenes_path = os.path.join(current_app.static_folder, 'OBS_Scenes.json')

    with open(scenes_path, 'r') as f:
        scenes_c = f.read()

    template = Template(scenes_c)
    data = {
        "user_id": str(current_user.id),
        "base_address": os.getenv('BASE_ADDRESS', 'http://localhost'),
    }
    scenes_json = template.render(data)
    response = make_response(scenes_json)
    response.headers['Content-Type'] = 'application/json'
    return response

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
def key(key):
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
            })
    
@main_bp.route('/api/keys/validate', methods=['POST'])
@csrf.exempt
def key_validate():
    key = request.form.get('name')
    if key:
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
    else:
        return jsonify({
                'status': 'Error',
                'data': None,
            }), 400
    
# @main_bp.route('/api/streams')
# def streams():
#     response = requests.get('http://nginx:8080/stat')
#     if response.status_code == 200:
#         streams = []
#         root = ET.fromstring(response.text)
#         for stream_key_el in root.findall(".//server/application/live/stream/name"):
#             user = User.query.filter_by(stream_key=stream_key_el.text).first()
#             if user:
#                 streams.append({"name": user.stream_name})

#         return jsonify({
#                 'status': 'success',
#                 'data': {
#                     'streams': streams,
#                 },
#             })
    
@main_bp.route('/api/streams/<int:stream_id>/overlay')
def stream(stream_id):
    user = User.query.filter_by(id=stream_id).first()
    if user:
        return render_template('stream_overlay.html', user=user)
    else:
        return "Stream name not found", 404
    
def get_streaming_users():
    users = []
    response = requests.get('http://nginx:8080/stat')
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        for stream_key_el in root.findall(".//server/application/live/stream/name"):
            user = User.query.filter_by(stream_key=stream_key_el.text).first()
            if user:
                users.append(user)

    return users