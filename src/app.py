from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# SQLAlchemy will use the database created at root
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Turns off Flask SQL Alchemy modification tracker, not the library's
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kelvin'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # auth

api.add_resource(Store, '/store/<string:name>')  # http://127.0.0.1:5000/item/..
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # debug for error messages (html page)
