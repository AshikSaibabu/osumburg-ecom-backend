import datetime
from app.extensions import db
from app.models.product_color_variant import ProductColorVariant
from app.models.size_varaint import SizeVariant
from app.models.sleeve_length_variant import SleeveLengthVariant


class ProductVariants(db.Model):
    __tablename__ = 'product_variant'

    id = db.Column(db.Integer, primary_key=True)
    color_variant = db.Column(db.Integer, db.ForeignKey('product_color_variant.id'))
    size_variant = db.Column(db.Integer, db.ForeignKey('size_variant.id'))
    sleeve_variant = db.Column(db.Integer, db.ForeignKey('sleeve_length_variant.id'))
    is_blocked = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

