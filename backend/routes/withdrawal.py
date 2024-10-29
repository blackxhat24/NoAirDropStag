from flask import Blueprint, jsonify, request
from ..models import db, User, Withdrawal
from ..web3_service import Web3Service
from decimal import Decimal

withdrawal_bp = Blueprint('withdrawal', __name__)
web3_service = Web3Service()

@withdrawal_bp.route('/api/withdraw', methods=['POST'])
async def withdraw():
    data = request.json
    user_id = data.get('user_id')
    wallet_address = data.get('wallet_address')
    amount = Decimal(str(data.get('amount', 0)))
    
    # Validate input
    if not all([user_id, wallet_address, amount]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate wallet address
    if not web3_service.validate_address(wallet_address):
        return jsonify({'error': 'Invalid wallet address'}), 400
    
    # Check minimum withdrawal
    if amount < 1:
        return jsonify({'error': 'Minimum withdrawal amount is 1 USDT'}), 400
    
    # Get user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check balance
    if user.usdt_balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400
    
    # Check admin wallet balance
    admin_balance = await web3_service.get_admin_balance()
    if admin_balance < float(amount):
        return jsonify({'error': 'Withdrawal temporarily unavailable'}), 503
    
    # Create withdrawal record
    withdrawal = Withdrawal(
        user_id=user_id,
        amount=amount,
        wallet_address=wallet_address,
        status='pending'
    )
    
    # Deduct balance from user
    user.usdt_balance -= amount
    
    try:
        db.session.add(withdrawal)
        db.session.commit()
        
        # Process withdrawal
        result = await web3_service.process_withdrawal(withdrawal)
        
        if result['success']:
            withdrawal.status = result['status']
            withdrawal.transaction_hash = result['transaction_hash']
        else:
            # Revert the balance deduction
            user.usdt_balance += amount
            withdrawal.status = 'failed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal processed',
            'status': withdrawal.status,
            'transaction_hash': withdrawal.transaction_hash if result['success'] else None
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@withdrawal_bp.route('/api/withdrawals/<int:user_id>', methods=['GET'])
def get_withdrawals(user_id):
    withdrawals = Withdrawal.query.filter_by(user_id=user_id).order_by(
        Withdrawal.timestamp.desc()
    ).all()
    
    return jsonify([{
        'id': w.id,
        'amount': float(w.amount),
        'status': w.status,
        'transaction_hash': w.transaction_hash,
        'timestamp': w.timestamp.isoformat()
    } for w in withdrawals])