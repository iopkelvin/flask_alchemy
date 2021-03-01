from flask_restful import Resource
from flask import request
from models.user import UserModel


class UserRegister(Resource):
    def post(self):
        data = request.get_json()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200