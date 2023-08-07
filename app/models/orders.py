import datetime
from app.extensions import db
from models.users import User
from models.cart import Cart
from models.product_variant import ProductVariants
from models.address import Address
from models.coupon import Coupon


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    billing_address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    coupon = db.Column(db.Integer, db.ForeignKey('coupon.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

