import datetime
from app.extensions import db
from models.users import User
from models.product_variant import ProductVariants
from models.orders import Order


class OrderItems(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'))
    qty = db.Column(db.Integer, default=1)
    sale_price = db.Column(db.Float)
    discount = db.Column(db.Float)
    tax = db.Column(db.Float)

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

