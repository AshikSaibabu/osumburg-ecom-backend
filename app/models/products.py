import datetime
from app.extensions import db
from models.category import Category
from models.type import Type
from models.design import Design


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    design_id = db.Column(db.Integer, db.ForeignKey('design.id'))
    name = db.Column(db.String(50))
    short_description = db.Column(db.String(500))
    long_description = db.Column(db.String(500))
    type = db.Column(db.Integer, db.ForeignKey('type.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    is_blocked = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Product "{self.name}">'

