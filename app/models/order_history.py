import datetime
from app.extensions import db
from models.users import User
from models.orders import Order
from models.delivery_status import DeliveryStatus


class OrderHistory(db.Model):
    __tablename__ = 'order_history'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.Integer, db.ForeignKey('delivery_status.id'))
    description = db.Column(db.String(1000))

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

