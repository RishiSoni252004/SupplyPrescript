/**
 * Main application component.
 *
 * Sets up the dashboard layout with Sidebar, TopNav, and main content area.
 */

import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <div className="app-layout">
      {/* Sidebar with mobile overlay */}
      <Sidebar />
      <div 
        className={`sidebar-overlay ${sidebarOpen ? 'sidebar-overlay--visible' : ''}`}
        onClick={closeSidebar}
      />
      <div className={`sidebar-container ${sidebarOpen ? 'sidebar-container--open' : ''}`}>
        <Sidebar />
      </div>

      <div className="main-wrapper">
        <TopNav onMenuToggle={toggleSidebar} />
        
        <main className="main-content">
          <Dashboard />
        </main>
      </div>
    </div>
  );
}

export default App;
