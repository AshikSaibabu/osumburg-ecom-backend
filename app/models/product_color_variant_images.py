import datetime
from app.extensions import db
from app.models.product_color_variant import ProductColorVariant


class ProductColorVariantImages(db.Model):
    __tablename__ = 'product_color_variant_images'

    id = db.Column(db.Integer, primary_key=True)
    color_variant = db.Column(db.Integer, db.ForeignKey('product_color_variant.id'))
    url = db.Column(db.String(1000))
    is_blocked = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

