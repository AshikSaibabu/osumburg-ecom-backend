import datetime
from app.extensions import db
from app.models.products import Product
from app.models.color_variant import ColorVariant


class ProductColorVariant(db.Model):
    """
        Maps products to color variants
    """
    __tablename__ = 'product_color_variant'

    id = db.Column(db.Integer, primary_key=True)
    color_variant = db.Column(db.Integer, db.ForeignKey('color_variant.id'))
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    is_blocked = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Product Color Variant "{self.product.id} {self.color_variant.id}">'

