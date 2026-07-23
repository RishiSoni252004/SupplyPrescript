/**
 * Sidebar component for the dashboard layout.
 *
 * Displays the application brand and navigation links.
 * The sidebar collapses to a top bar on mobile screens.
 */

import React from 'react';
import {
  HiOutlineViewGrid,
  HiOutlineTruck,
  HiOutlineCog,
  HiOutlineSupport,
} from 'react-icons/hi';
import { HiOutlineCube } from 'react-icons/hi2';
import './Sidebar.css';

const navItems = [
  { icon: <HiOutlineViewGrid />, label: 'Dashboard', active: true },
  { icon: <HiOutlineTruck />, label: 'Shipments', active: false },
  { icon: <HiOutlineCube />, label: 'Inventory', active: false },
  { icon: <HiOutlineCog />, label: 'Settings', active: false },
  { icon: <HiOutlineSupport />, label: 'Support', active: false },
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
              <a
                href="#"
                className={`nav-link ${item.active ? 'nav-link--active' : ''}`}
                id={`nav-${item.label.toLowerCase()}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </a>
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
