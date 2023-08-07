import datetime
from app.extensions import db


class ColorVariant(db.Model):
    __tablename__ = 'color_variant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    hex_code = db.Column(db.String(6))
    is_blocked = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Color "{self.name}">'

