from web3 import Web3
from eth_account import Account
import json
from .config import Config

class Web3Service:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(Config.WEB3_PROVIDER_URI))
        self.admin_account = Account.from_key(Config.ADMIN_PRIVATE_KEY)
        
        # USDT Contract ABI (minimal ABI for transfers)
        self.usdt_abi = json.loads('''[
            {
                "constant": false,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            },
            {
                "constant": true,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }
        ]''')
        
        self.usdt_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(Config.USDT_CONTRACT_ADDRESS),
            abi=self.usdt_abi
        )

    def validate_address(self, address):
        """Validate if the address is a valid BSC address."""
        try:
            return Web3.is_address(address) and Web3.to_checksum_address(address)
        except:
            return False

    async def process_withdrawal(self, withdrawal):
        """Process a withdrawal transaction."""
        try:
            # Get the nonce
            nonce = self.w3.eth.get_transaction_count(self.admin_account.address)
            
            # Convert amount to USDT decimals (6 decimals)
            amount_wei = int(float(withdrawal.amount) * 10**6)
            
            # Prepare the transaction
            transaction = self.usdt_contract.functions.transfer(
                Web3.to_checksum_address(withdrawal.wallet_address),
                amount_wei
            ).build_transaction({
                'chainId': 56,  # BSC mainnet
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            # Sign the transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, 
                private_key=Config.ADMIN_PRIVATE_KEY
            )
            
            # Send the transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': receipt['transactionHash'].hex(),
                'status': 'completed' if receipt['status'] == 1 else 'failed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 'failed'
            }

    async def get_admin_balance(self):
        """Get the USDT balance of the admin wallet."""
        balance = self.usdt_contract.functions.balanceOf(
            self.admin_account.address
        ).call()
        return balance / 10**6  # Convert from wei to USDT