import datetime
from app.extensions import db
from models.design import Design


class DesignAssets(db.Model):
    __tablename__ = 'design_assets'

    id = db.Column(db.Integer, primary_key=True)
    design_id = db.Column(db.Integer, db.ForeignKey('design.id'))
    url = db.Column(db.String(1000))
    is_blocked = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

