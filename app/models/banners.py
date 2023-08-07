import datetime
from app.extensions import db
from models.users import User


class Banners(db.Model):
    __tablename__ = 'banners'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    link = db.Column(db.String(200))
    description = db.Column(db.String(1000))

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

