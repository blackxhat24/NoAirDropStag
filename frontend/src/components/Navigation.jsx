import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  UserIcon, 
  UserGroupIcon, 
  CurrencyDollarIcon 
} from '@heroicons/react/24/outline';

const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: HomeIcon, label: 'Game' },
    { path: '/profile', icon: UserIcon, label: 'Profile' },
    { path: '/invite', icon: UserGroupIcon, label: 'Invite' },
    { path: '/withdraw', icon: CurrencyDollarIcon, label: 'Withdraw' }
  ];

  return (
    <nav className="bg-white border-t border-gray-200">
      <div className="flex justify-around">
        {navItems.map(({ path, icon: Icon, label }) => (
          <Link
            key={path}
            to={path}
            className={`flex flex-col items-center p-4 ${
              location.pathname === path ? 'text-blue-600' : 'text-gray-500'
            }`}
          >
            <Icon className="w-6 h-6" />
            <span className="text-xs mt-1">{label}</span>
          </Link>
        ))}
      </div>
    </nav>
  );
};

export default Navigation;
