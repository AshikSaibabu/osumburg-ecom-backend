import datetime
from app.extensions import db
from app.models.users import User


class PODVendors(db.Model):
    __tablename__ = 'pod_vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class ShippingCost(db.Model):
    __tablename__ = 'shipping_cost'

    id = db.Column(db.Integer, primary_key=True)
    pod_vendor_id = db.Column(db.Integer, db.ForeignKey('pod_vendors.id'))
    shipping_cost = db.Column(db.Integer, default=0, nullable=False)
    shipping_cost_weight_slab = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

