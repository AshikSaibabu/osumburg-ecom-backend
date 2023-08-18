import datetime
from app.extensions import db
from models.product_variant import ProductVariants


class PrintroveProduct(db.Model):
    __tablename__ = 'printrove_product'

    id = db.Column(db.Integer, primary_key=True)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'))
    printrove_product_id = db.Column(db.Integer, nullable=False)
    printrove_variant_id = db.Column(db.Integer, nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

