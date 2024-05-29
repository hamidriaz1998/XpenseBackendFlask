from app import app, db
from Models.User import UserModel
from flask import request, jsonify
import bcrypt

@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        data = request.get_json()
        hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = UserModel(name=data['name'], email=data['email'], password_hash=hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created!'}), 201
    elif request.method == 'GET':
        users = UserModel.query.all()
        return jsonify([user.to_dict() for user in users])