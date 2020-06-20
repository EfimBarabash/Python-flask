from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    response = {'response': 'index response'}
    return jsonify(response)

@main.route('/profile')
@login_required
def profile():
    a = current_user
    return jsonify({
        'email': current_user.email
    })