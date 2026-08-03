/**
 * Sidebar component for the dashboard layout.
 *
 * Displays the application brand and navigation links.
 * The sidebar collapses to a top bar on mobile screens.
 */

import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  HiOutlineViewGrid,
  HiOutlineTruck,
} from 'react-icons/hi';
import { HiOutlineChartBar } from 'react-icons/hi2';
import './Sidebar.css';

const navItems = [
  { icon: <HiOutlineViewGrid />, label: 'Dashboard', path: '/' },
  { icon: <HiOutlineTruck />, label: 'Shipments', path: '/shipments' },
  { icon: <HiOutlineChartBar />, label: 'Prediction & Recs', path: '/prediction' },
  { icon: <HiOutlineChartBar />, label: 'Analytics', path: '/analytics' },
];

const Sidebar = () => {
  return (
    <aside className="sidebar" id="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo">
          <span className="logo-icon">⚡</span>
        </div>
        <span className="brand-name">SupplyPrescript</span>
      </div>

      <nav className="sidebar-nav">
        <ul className="nav-list">
          {navItems.map((item) => (
            <li key={item.label}>
              <NavLink
                to={item.path}
                className={({ isActive }) => `nav-link ${isActive ? 'nav-link--active' : ''}`}
                id={`nav-${item.label.toLowerCase().replace(/[^a-z0-9]/g, '-')}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-version">v1.0.0</div>
      </div>
    </aside>
  );
};

export default Sidebar;
