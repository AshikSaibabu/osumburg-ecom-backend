import datetime
from app.extensions import db
from models.users import User
from models.reviews import Reviews


class ReviewAssets(db.Model):
    __tablename__ = 'review_assets'

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))
    url = db.Column(db.String(1000))
    is_deleted = db.Column(db.Boolean(), default=False)
    is_censored = db.Column(db.Boolean(), default=False)

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

