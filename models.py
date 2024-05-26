from main import db
from sqlalchemy.dialects.postgresql import JSON
from flask_login import LoginManager, UserMixin, login_user, logout_user



class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
 