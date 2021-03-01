from flask import request, jsonify
from flask_restful import Resource
from flask_jwt import jwt_required
from models.item import ItemModel, ItemSchema
from marshmallow import ValidationError  # To raise errors from Marshmallow schema


class Item(Resource):  # inheritance
    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)  # queries table and returns first, by parameter
        if item:
            return item.json()  # json format response (can modify model)
        return {'message': 'Item not found'}, 404  # Not Found

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # bad request
        json_data = request.get_json()

        try:  # Make sure that input in equal to schema
            data = ItemSchema().load(json_data)
        except ValidationError as err:
            response = jsonify(err.messages)
            response.status_code = 422
            return response

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except ValueError:
            return {"message": "An error occurred inserting the item."}, 500  # Internal server error

        return item.json(), 201  # created status code

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}, 404

    def put(self, name):
        json_data = request.get_json()

        item = ItemModel.find_by_name(name)
        # Item is already there, but characteristics will be modified
        if item:  # Specify which parameters will be modified
            item.price = json_data['price']
            item.save_to_db()

        else:
            try:  # Make sure that input in equal to schema
                data = ItemSchema().load(json_data)
            except ValidationError as err:
                response = jsonify(err.messages)
                response.status_code = 422
                return response
            item = ItemModel(name, **data)
            item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # List comprehensions version
        return {'items': [item.json() for item in ItemModel.find_all()]}
