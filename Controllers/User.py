from flask import request, jsonify, Blueprint
from extensions import db
from Models.User import UserModel
import bcrypt  # for salting and hashing passwords
from sqlalchemy.exc import IntegrityError # for handling unique constraint violation

bp = Blueprint('user', __name__)

@bp.route('/signUp', methods=['POST'])
def sign_up():
    data = request.get_json()
    if not all(key in data for key in ('name', 'email', 'password')):
        return jsonify({'message': 'Invalid request!'}), 400
    if len(data["password"]) < 6:
        return jsonify({'message': 'Password must be at least 6 characters long!'}), 400
    hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = UserModel(name=data['name'], email=data['email'], password_hash=hash)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'message': 'User already exists!'}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error!'}), 500
    return jsonify({'message': 'User created!'}), 201

@bp.route('/signIn', methods=['POST'])
def sign_in():
    data = request.get_json()
    if not all(key in data for key in ('email', 'password')):
        return jsonify({'message': 'Invalid request!'}), 400
    try:
        user = UserModel.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        if bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
            return jsonify({"message": "User logged in successfully", "user": user.to_dict()}), 200
        else:
            return jsonify({'message': 'Invalid password!'}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error!'}), 500

@bp.route('/changePass', methods=['POST'])
def change_pass():
    data = request.get_json()
    if not all(key in data for key in ('email', 'oldPassword', 'newPassword')):
        return jsonify({'message': 'Invalid request!'}), 400
    try:
        user = UserModel.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        if bcrypt.checkpw(data['oldPassword'].encode('utf-8'), user.password_hash.encode('utf-8')):
            if len(data["newPassword"]) < 6:
                return jsonify({'message': 'Password must be at least 6 characters long!'}), 400
            hash = bcrypt.hashpw(data['newPassword'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password_hash = hash
            db.session.commit()
            return jsonify({'message': 'Password changed!'}), 200
        else:
            return jsonify({'message': 'Invalid password!'}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error!'}), 500
