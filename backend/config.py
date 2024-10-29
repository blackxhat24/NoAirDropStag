import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/noairdrop')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Telegram configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_WEBAPP_URL = os.getenv('TELEGRAM_WEBAPP_URL')
    
    # Blockchain configuration
    WEB3_PROVIDER_URI = os.getenv('WEB3_PROVIDER_URI', 'https://bsc-dataseed.binance.org/')
    USDT_CONTRACT_ADDRESS = os.getenv('USDT_CONTRACT_ADDRESS')
    ADMIN_WALLET_ADDRESS = os.getenv('ADMIN_WALLET_ADDRESS')
    ADMIN_PRIVATE_KEY = os.getenv('ADMIN_PRIVATE_KEY')