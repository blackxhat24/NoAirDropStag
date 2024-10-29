from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    usdt_balance = db.Column(db.Numeric(20, 6), default=0)
    total_clicks = db.Column(db.Integer, default=0)
    wallet_address = db.Column(db.String(42))  # Ethereum wallet address
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_click_time = db.Column(db.DateTime)
    referral_code = db.Column(db.String(20), unique=True)
    
    # Relationships
    clicks = db.relationship('Click', backref='user', lazy=True)
    withdrawals = db.relationship('Withdrawal', backref='user', lazy=True)
    referrals = db.relationship('Referral', backref='referrer', lazy=True, foreign_keys='Referral.referrer_id')

class Click(db.Model):
    __tablename__ = 'clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(20, 6), nullable=False)  # Amount earned from click
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Withdrawal(db.Model):
    __tablename__ = 'withdrawals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(20, 6), nullable=False)
    wallet_address = db.Column(db.String(42), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    transaction_hash = db.Column(db.String(66))  # Blockchain transaction hash
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Referral(db.Model):
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bonus_amount = db.Column(db.Numeric(20, 6), default=0.1)  # 0.1 USDT bonus
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, completed