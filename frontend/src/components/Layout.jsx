import React from 'react';
import { Outlet } from 'react-router-dom';
import Navigation from './Navigation';

const Layout = () => {
  return (
    <div className="flex flex-col h-[100vh] bg-gray-100">
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
      <Navigation />
    </div>
  );
};

export default Layout;