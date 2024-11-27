from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from argon2 import PasswordHasher
import secrets
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ph = PasswordHasher(time_cost=3, memory_cost=65536)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mdss.db"

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.main_bp)
        db.create_all()

        if not User.query.first():
            db.session.add(User(username="test", password=ph.hash("test")))
            db.session.commit()

    return app
