/**
 * Main application component.
 *
 * Sets up the dashboard layout with Sidebar, TopNav, and main content area.
 */

import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import Dashboard from './pages/Dashboard';
import ShipmentList from './pages/shipment/ShipmentList';
import ShipmentForm from './pages/shipment/ShipmentForm';
import PredictionPage from './pages/prediction/PredictionPage';
import AnalyticsDashboard from './pages/analytics/AnalyticsDashboard';
import SettingsPage from './pages/settings/SettingsPage';
import DecisionHistory from './pages/decisions/DecisionHistory';
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
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/shipments" element={<ShipmentList />} />
            <Route path="/shipments/add" element={<ShipmentForm />} />
            <Route path="/shipments/edit/:id" element={<ShipmentForm />} />
            <Route path="/prediction" element={<PredictionPage />} />
            <Route path="/analytics" element={<AnalyticsDashboard />} />
            <Route path="/decisions" element={<DecisionHistory />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
      <ToastContainer position="bottom-right" />
    </div>
  );
}

export default App;
