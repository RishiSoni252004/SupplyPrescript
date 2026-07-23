/**
 * Top navigation bar component.
 *
 * Displays the page title, a search input, and user actions.
 */

import React from 'react';
import { HiOutlineBell, HiOutlineSearch } from 'react-icons/hi';
import { HiOutlineBars3 } from 'react-icons/hi2';
import './TopNav.css';

const TopNav = ({ onMenuToggle }) => {
  return (
    <header className="topnav" id="topnav">
      <div className="topnav-left">
        <button
          className="topnav-menu-btn"
          onClick={onMenuToggle}
          aria-label="Toggle sidebar menu"
          id="menu-toggle-btn"
        >
          <HiOutlineBars3 />
        </button>
        <div className="topnav-title">
          <h1>Dashboard</h1>
          <p className="topnav-subtitle">Supply Chain Analytics Overview</p>
        </div>
      </div>

      <div className="topnav-right">
        <div className="topnav-search" id="topnav-search">
          <HiOutlineSearch className="search-icon" />
          <input
            type="text"
            placeholder="Search shipments…"
            className="search-input"
            id="search-input"
          />
        </div>

        <button className="topnav-icon-btn" aria-label="Notifications" id="notifications-btn">
          <HiOutlineBell />
          <span className="notification-badge">3</span>
        </button>

        <div className="topnav-avatar" id="user-avatar">
          <span className="avatar-initials">RP</span>
        </div>
      </div>
    </header>
  );
};

export default TopNav;
