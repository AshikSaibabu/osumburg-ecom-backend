import datetime
from app.extensions import db
from models.users import User
from models.coupon_type import CouponType


class Coupon(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    discount_percentage = db.Column(db.Integer, default=0)
    type = db.Column(db.Integer, db.ForeignKey('coupon_type.id'))
    is_valid = db.Column(db.Boolean(), default=False)
    min_purchase_amount = db.Column(db.Integer)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

