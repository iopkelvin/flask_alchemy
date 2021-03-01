from db import db
# from marshmallow import Schema, fields, ValidationError
from app import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)
# class ItemSchema(Schema):
#     name = fields.String(required=True)
#     price = fields.Float(required=True)
#     store_id = fields.Integer(required=True)


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'price': self.price,
                'store_id': self.store_id
                }

    @classmethod  # Inherits from class (item)
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class ItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ItemModel

    # name = ma.auto_field()
    # price = ma.auto_field()
    # store_id = ma.auto_field()