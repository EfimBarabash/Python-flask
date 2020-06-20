from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():

    email = request.json.get('email')
    password = request.json.get('password')
    remember = True if request.json.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'status': 'invalid credentials'})

    login_user(user, remember=remember)
    return jsonify({'status': 'Success'})


@auth.route('/signup')
def signup():
    return 'Signup'


@auth.route('/logout')
def logout():
    return 'Logout'


@auth.route('/signup', methods=['POST'])
def signup_post():
    a = request
    email = request.json.get('email')
    name = request.json.get('name')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return jsonify({'status': 'Error'})

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 'Success'})
