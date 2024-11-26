from app import db
import app.keygen as keygen
from flask_login import UserMixin

def default_stream_name(context):
    return f"{context.get_current_parameters()['username']}'s stream"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    stream_key = db.Column(db.String(150), unique=True, nullable=False, default=keygen.generate_key())
    stream_name = db.Column(db.String(150), nullable=False, default=default_stream_name)
