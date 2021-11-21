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
class Message_Table(db.Model):
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


@app.route('/user/register', methods=['POST'])
def register():

    if not request.is_json:
        return jsonify({'message': 'body must be a json , got: ' + request.get_data().decode('utf-8'),
            'status': 400}), 400
    
    body = request.get_json()

    if 'email' not in body or 'name' not in body or 'password' not in body:
        return jsonify({'message': 'body must be a json contains: email, name and password, got: ' + str(body),
                'status': 400}), 400
    
    email = body['email']
    name = body['name']
    password = body['password']

    # if it returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first() 
    if user:
        return jsonify({"message": f"user already exist with email {email}"}), 400

    # create a new user and hash the password so the original password isn't saved
    new_user = User(email=email,
                    name=name,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # returns the user means successfully registered
    return jsonify(new_user)


@app.route('/user/login/<email>/<password>', methods=['GET'])
def login(email, password):

    user = User.query.filter_by(email=email).first()
    print(f'user = {user}')

    # check if the user is exists then take a given password, hash it and compare it to 
    # the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "invalid credentials"})

    login_user(user)
    # returns the user means successfully loged in
    return jsonify(user)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


if __name__ == "__main__":
    
    if not os.path.exists(DATABASE_NAME):
        db.create_all()

    app.run(debug=True)