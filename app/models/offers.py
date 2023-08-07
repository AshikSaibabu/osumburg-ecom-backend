import datetime
from app.extensions import db
from models.users import User


class Offers(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    discount_percentage = db.Column(db.Float, default=0)
    description = db.Column(db.String(1000))
    is_valid = db.Column(db.Boolean(), default=False)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

