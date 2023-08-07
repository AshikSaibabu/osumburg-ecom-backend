import datetime
from app.extensions import db
from models.users import User
from models.products import Product
from models.offers import Offers


class AppliedOffers(db.Model):
    __tablename__ = 'applied_offers'

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    is_deleted = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

