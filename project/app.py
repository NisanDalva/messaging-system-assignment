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


if __name__ == "__main__":
    
    if not os.path.exists(DATABASE_NAME):
        db.create_all()

    app.run(debug=True)