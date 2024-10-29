import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { WebApp } from '@twa-dev/sdk';
import Layout from './components/Layout';
import Game from './components/Game';
import Profile from './components/Profile';
import Invite from './components/Invite';
import Withdraw from './components/Withdraw';

function App() {
  React.useEffect(() => {
    // Initialize Telegram WebApp
    WebApp.ready();
    // Set viewport height for mobile
    document.documentElement.style.setProperty(
      '--vh',
      `${window.innerHeight * 0.01}px`
    );
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Game />} />
          <Route path="profile" element={<Profile />} />
          <Route path="invite" element={<Invite />} />
          <Route path="withdraw" element={<Withdraw />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;