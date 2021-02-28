import sqlite3
from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):  # inheritance
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404  # Not Found

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # bad request

        data = request.get_json()
        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except ValueError:
            return {"message": "An error occurred inserting the item."}, 500  # Internal server error

        return item.json(), 201  # created status code

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

    def put(self, name):
        data = request.get_json()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
