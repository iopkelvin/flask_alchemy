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