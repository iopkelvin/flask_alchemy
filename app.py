import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT  # Security

from security import authenticate, identity  # Modules for JWT
from resources.user import UserRegister, User  # To authenticate
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['DEBUG'] = True  # debug for error messages (html page)

# SQLAlchemy will use the database created at root or sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# Turns off Flask SQL Alchemy modification tracker, not the library's
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Allows flask extensions to raise their own exceptions/errors
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kelvin'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # auth

api.add_resource(Store, '/store/<string:name>')  # http://127.0.0.1:5000/item/..
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    # If app.py is run, then the following will be run.
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)