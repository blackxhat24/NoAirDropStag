import React from 'react';
import { WebApp } from '@twa-dev/sdk';

const Invite = () => {
  const handleShare = () => {
    WebApp.switchInlineQuery(
      `Join NoAirDrop and earn USDT! Use my referral code: ${WebApp.initDataUnsafe?.user?.id}`,
      ['']
    );
  };

  return (
    <div className="p-4">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Invite Friends</h2>
        
        <div className="mb-6">
          <p className="text-gray-600 mb-2">
            Share with friends and earn 0.1 USDT for each referral!
          </p>
          
          <div className="bg-gray-50 p-4 rounded-lg mb-4">
            <p className="text-sm text-gray-500">Your Referral Code</p>
            <p className="text-lg font-mono">{WebApp.initDataUnsafe?.user?.id}</p>
          </div>
        </div>

        <button
          onClick={handleShare}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Share with Friends
        </button>
      </div>
    </div>
  );
};

export default Invite;