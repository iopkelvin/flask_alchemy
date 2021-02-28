import sqlite3
from flask_restful import Resource
from flask import request
from models.user import UserModel


class UserRegister(Resource):
    def post(self):
        data = request.get_json()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201