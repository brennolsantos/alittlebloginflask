from flask import Blueprint, request, jsonify, session, make_response
from project.app import db 
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()     

    if not user or not check_password_hash(user.password, password):
        res = {
            'status': 'Login failed'
        }

        return make_response(jsonify(res), 400) 

    res = {
        'status': 'Success'
    }

    login_user(user)
    return make_response(jsonify(res()),200) 
   


@auth.route('/signup', methods=['POST'])
def signup():

    email = request.form['email']
    name = request.form['name']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user:
        res = {
            'status': 'User already exists'
        }    

        return make_response(jsonify(res), 400)
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    res = {
        'status': 'Success '
    }

    return make_response(jsonify(res),200)

@auth.route('/logout')
@login_required
def logout():
    
    logout_user()
    
    res = {
        'status': 'Logged out'
    }

    return make_response(jsonify(res), 200)


@auth.route('/user')
def get_user():
    name = request.form['name']

    user = User.query.filter_by(name=name).first()

    if not user:
        res = {
            'Status': 'User doesn\'t exist'
        }
        return make_response(jsonify(res), 400)

    res = {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }

    return make_response(jsonify(res), 200)



@auth.route('/getuserid')
def cur_user_id():
    res = {
        'id': current_user.id
    }

    return make_response(res, 200)
