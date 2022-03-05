from . import db
from flask_login import UserMixin

class FollowedCurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    currencies = db.relationship('FollowedCurrency')

class MarketCurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.String)
    change24h = db.Column(db.String)
    color24h = db.Column(db.String)
    change7d = db.Column(db.String)
    color7d = db.Column(db.String)

class SliderCurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.String)
    change = db.Column(db.String)
    color = db.Column(db.String)