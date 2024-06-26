from flask import request, jsonify, Blueprint
from extensions import db
from Models.User import UserModel
from extensions import bcrypt
from sqlalchemy.exc import IntegrityError # for handling unique constraint violation

bp = Blueprint('user', __name__)

@bp.route('/signUp', methods=['POST'])
def sign_up():
    data = request.get_json()
    if not all(key in data for key in ('name', 'email', 'password')):
        return jsonify({'message': 'Invalid request!'}), 400
    if len(data["password"]) < 6:
        return jsonify({'message': 'Password must be at least 6 characters long!'}), 400
    hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
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
        if user.check_password(data['password']):
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

@bp.route('/update-user', methods=['PUT'])
def update_user():
    data = request.get_json()
    if not all(key in data for key in ('id', 'name', 'email')):
        return jsonify({'message': 'Invalid request!'}), 400
    try:
        user = UserModel.query.filter_by(id=data['id']).first()
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        user.name = data['name']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error!'}), 500

@bp.route('/delete-user/<int:id>', methods=['DELETE'])
def delete_user(id:int):
    try:
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error!'}), 500
    
@bp.route('/get-users', methods=['GET'])
def get_users():
    try:
        users = UserModel.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error!'}), 500