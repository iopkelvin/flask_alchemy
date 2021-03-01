# This file will be run first. It instantiates the database with the app, then it creates the tables.

from app import app
from db import db

# The init_app method exists so that the database object can be instantiated without requiring an app object.
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()