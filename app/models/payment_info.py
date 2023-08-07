import datetime
import enum
from app.extensions import db
from models.users import User
from models.orders import Order
from models.delivery_status import DeliveryStatus
from models.payment_methods import PaymentMethods


class PaymentStatus(enum.Enum):
    success = 1
    failed = 2


class PaymentInfo(db.Model):
    __tablename__ = 'payment_info'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    amount = db.Column(db.Float)
    payment_method = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    status = value = db.Column(db.Enum(PaymentStatus))
    ref_num = db.Column(db.String(100))

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

