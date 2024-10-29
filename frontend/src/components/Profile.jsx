import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { WebApp } from '@twa-dev/sdk';

const Profile = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get(`/api/user/${WebApp.initDataUnsafe?.user?.id}/profile`);
        setProfile(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  if (!profile) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center mb-6">
          <img
            src={WebApp.initDataUnsafe?.user?.photo_url || '/default-avatar.png'}
            alt="Profile"
            className="w-16 h-16 rounded-full"
          />
          <div className="ml-4">
            <h2 className="text-xl font-bold">{profile.username}</h2>
            <p className="text-gray-500">
              {profile.first_name} {profile.last_name}
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="border-t pt-4">
            <p className="text-gray-500">Balance</p>
            <p className="text-2xl font-bold">{profile.usdt_balance.toFixed(6)} USDT</p>
          </div>

          <div className="border-t pt-4">
            <p className="text-gray-500">Total Clicks</p>
            <p className="text-2xl font-bold">{profile.total_clicks}</p>
          </div>

          <div className="border-t pt-4">
            <p className="text-gray-500">Referral Code</p>
            <p className="text-xl font-mono">{profile.referral_code}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;