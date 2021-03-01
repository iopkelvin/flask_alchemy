from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Turns off Flask SQL Alchemy modification tracker, not the library's
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kelvin'
api = Api(app)

# db.init_app(app)
@app.before_first_request():
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # auth

api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/..
api.add_resource(StoreList, '/stores')
api.add_resource(Item, 'item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # debug for error messages (html page)
