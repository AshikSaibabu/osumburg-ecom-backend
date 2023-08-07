import datetime
from app.extensions import db
from models.users import User


class DeliveryStatus(db.Model):
    __tablename__ = 'delivery_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(25))

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

