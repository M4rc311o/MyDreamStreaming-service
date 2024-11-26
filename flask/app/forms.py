from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')

class StreamInfoForm(FlaskForm):
    name = StringField('Stream name', validators=[DataRequired()])
    save = SubmitField('Save')

class StreamKeyForm(FlaskForm):
    key = PasswordField('Stream key', render_kw={'readonly': True}, widget=PasswordInput(hide_value=False))