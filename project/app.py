import os
from datetime import datetime
from dataclasses import dataclass

from flask import Flask, jsonify, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_NAME = 'database.db'
app = Flask(__name__)

# since 'SECRET_KEY' is obviously needs to be secret, no need to put it on a public repository,
# read it from the environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'

db = SQLAlchemy(app)
login_manager = LoginManager()

login_manager.init_app(app)


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id: int
    email: str
    password: str
    name: str

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(100))


@dataclass
class Message_Table(db.Model, Base):
    __tablename__ = 'message'
    __table_args__ = (ForeignKeyConstraint(['sender', 'receiver'], ['user.id', 'user.id']),)
    id: int
    sender: int
    receiver: int
    message: str
    subject: str
    creation_date: datetime
    did_read: bool

    id = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey('user.id'), nullable=False)
    receiver = Column(Integer, ForeignKey('user.id'), nullable=False)
    message = Column(String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    did_read = Column(Boolean, default=False)
    
    sender_relationship = relationship("User", foreign_keys=[sender])
    receiver_relationship = relationship("User", foreign_keys=[receiver]) 

if __name__ == "__main__":
    
    if not os.path.exists(DATABASE_NAME):
        db.create_all()

    app.run(debug=True)