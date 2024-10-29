from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import telegram
from telegram import WebAppInfo
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import json
import logging

from .config import Config
from .models import db, User, Click, Withdrawal, Referral

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Initialize Telegram bot
    bot = telegram.Bot(token=Config.TELEGRAM_BOT_TOKEN)
    
    # Routes
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow()})
    
    @app.route('/api/user/register', methods=['POST'])
    def register_user():
        data = request.json
        telegram_id = data.get('telegram_id')
        
        if not telegram_id:
            return jsonify({'error': 'Telegram ID is required'}), 400
            
        existing_user = User.query.filter_by(telegram_id=telegram_id).first()
        if existing_user:
            return jsonify({'message': 'User already registered', 'user_id': existing_user.id}), 200
            
        new_user = User(
            telegram_id=telegram_id,
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id
        }), 201
    
    @app.route('/api/click', methods=['POST'])
    def record_click():
        data = request.json
        user_id = data.get('user_id')
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Check if enough time has passed since last click (anti-spam)
        if user.last_click_time and \
           datetime.utcnow() - user.last_click_time < timedelta(seconds=1):
            return jsonify({'error': 'Please wait before clicking again'}), 429
        
        # Record click and update balance
        click_amount = 0.00001  # USDT per click
        
        click = Click(
            user_id=user_id,
            amount=click_amount
        )
        
        user.usdt_balance = float(user.usdt_balance or 0) + click_amount
        user.total_clicks += 1
        user.last_click_time = datetime.utcnow()
        
        db.session.add(click)
        db.session.commit()
        
        return jsonify({
            'message': 'Click recorded',
            'new_balance': float(user.usdt_balance)
        })
    
    @app.route('/api/user/<int:user_id>/profile')
    def get_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'usdt_balance': float(user.usdt_balance or 0),
            'total_clicks': user.total_clicks,
            'referral_code': user.referral_code
        })
    
    # Telegram bot command handlers
    def start(update, context):
        """Send a message when the command /start is issued."""
        keyboard = [
            [telegram.KeyboardButton("🎮 Play Game", web_app=WebAppInfo(url=Config.TELEGRAM_WEBAPP_URL))],
            [telegram.KeyboardButton("❓ FAQ"), telegram.KeyboardButton("🌐 Official Website")]
        ]
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        welcome_message = (
            "Welcome to NoAirDrop! 🎮\n\n"
            "Click to earn USDT! Each click earns you 0.00001 USDT.\n"
            "Invite friends to earn bonus rewards!\n\n"
            "Click 'Play Game' to start earning!"
        )
        
        update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    def faq(update, context):
        """Send FAQ information."""
        faq_text = (
            "❓ Frequently Asked Questions\n\n"
            "1. How do I earn USDT?\n"
            "   - Click the logo in the game to earn 0.00001 USDT per click\n\n"
            "2. How do I withdraw?\n"
            "   - Go to the withdrawal section and enter your wallet address\n"
            "   - Minimum withdrawal: 1 USDT\n\n"
            "3. How does the referral system work?\n"
            "   - Share your referral link with friends\n"
            "   - Earn 0.1 USDT for each new user who joins\n\n"
            "4. Is this free?\n"
            "   - Yes! No investment required"
        )
        update.message.reply_text(faq_text)
    
    # Set up Telegram bot handlers
    updater = Updater(token=Config.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("faq", faq))
    
    # Start the bot
    updater.start_polling()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, ssl_context='adhoc')