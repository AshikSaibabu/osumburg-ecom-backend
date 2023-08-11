import datetime
from app.extensions import db
from app.models.product_variant import ProductVariants


class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)
    product_variant = db.Column(db.Integer, db.ForeignKey('product_variant.id'))
    qty = db.Column(db.Integer, default=0)
    is_pod = db.Column(db.Boolean(), default=False)
    is_blocked = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

