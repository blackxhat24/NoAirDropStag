import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { WebApp } from '@twa-dev/sdk';

const Game = () => {
  const [balance, setBalance] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [lastClickTime, setLastClickTime] = useState(0);

  const handleClick = async () => {
    const now = Date.now();
    if (now - lastClickTime < 1000) return; // Rate limiting

    setIsAnimating(true);
    setLastClickTime(now);

    try {
      const response = await axios.post('/api/click', {
        user_id: WebApp.initDataUnsafe?.user?.id
      });
      
      setBalance(response.data.new_balance);
      
      // Show earning animation
      const earnDiv = document.createElement('div');
      earnDiv.className = 'earning-animation';
      earnDiv.textContent = '+0.00001 USDT';
      document.getElementById('game-container').appendChild(earnDiv);
      
      setTimeout(() => {
        earnDiv.remove();
        setIsAnimating(false);
      }, 1000);
    } catch (error) {
      console.error('Click error:', error);
      setIsAnimating(false);
    }
  };

  return (
    <div id="game-container" className="flex flex-col items-center justify-center h-full relative">
      <div className="text-2xl font-bold mb-8">
        {balance.toFixed(6)} USDT
      </div>
      
      <button
        onClick={handleClick}
        disabled={isAnimating}
        className={`transform transition-transform active:scale-95 ${
          isAnimating ? 'opacity-50' : ''
        }`}
      >
        <img
          src="/logo.svg"
          alt="Click to earn"
          className="w-48 h-48"
        />
      </button>
      
      <div className="mt-8 text-sm text-gray-500">
        Tap to earn 0.00001 USDT
      </div>
    </div>
  );
};

export default Game;