import React, { useState } from 'react';
import axios from 'axios';
import { WebApp } from '@twa-dev/sdk';

const Withdraw = () => {
  const [walletAddress, setWalletAddress] = useState('');
  const [amount, setAmount] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleWithdraw = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/withdraw', {
        user_id: WebApp.initDataUnsafe?.user?.id,
        wallet_address: walletAddress,
        amount: parseFloat(amount)
      });

      WebApp.showAlert('Withdrawal request submitted successfully!');
      setWalletAddress('');
      setAmount('');
    } catch (error) {
      setError(error.response?.data?.error || 'Something went wrong');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Withdraw USDT</h2>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleWithdraw}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">
              Wallet Address (BSC)
            </label>
            <input
              type="text"
              value={walletAddress}
              onChange={(e) => setWalletAddress(e.target.value)}
              className="w-full p-3 border rounded"
              placeholder="Enter your BSC wallet address"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 mb-2">
              Amount (USDT)
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="w-full p-3 border rounded"
              placeholder="Minimum: 1 USDT"
              min="1"
              step="0.000001"
              required
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full bg-blue-600 text-white py-3 rounded-lg font-medium ${
              isLoading ? 'opacity-50' : 'hover:bg-blue-700'
            } transition-colors`}
          >
            {isLoading ? 'Processing...' : 'Withdraw'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Withdraw;