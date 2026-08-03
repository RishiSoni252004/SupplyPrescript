import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import { toast } from 'react-toastify';
import './SettingsPage.css';

const SettingsPage = () => {
  const { isDarkMode, toggleTheme } = useTheme();

  const handleSave = () => {
    toast.success('Settings saved successfully.');
  };

  return (
    <div className="settings-container fade-in">
      <div className="settings-header">
        <h1>Settings</h1>
        <p>Manage your preferences and application settings.</p>
      </div>

      <div className="settings-grid">
        <div className="settings-card glass-panel">
          <h2>Appearance</h2>
          <div className="setting-item">
            <div>
              <h3>Dark Mode</h3>
              <p>Toggle dark mode for the application interface.</p>
            </div>
            <label className="toggle-switch">
              <input type="checkbox" checked={isDarkMode} onChange={toggleTheme} />
              <span className="slider round"></span>
            </label>
          </div>
        </div>

        <div className="settings-card glass-panel">
          <h2>Notifications</h2>
          <div className="setting-item">
            <div>
              <h3>Email Alerts</h3>
              <p>Receive email notifications for delayed shipments.</p>
            </div>
            <label className="toggle-switch">
              <input type="checkbox" defaultChecked />
              <span className="slider round"></span>
            </label>
          </div>
          <div className="setting-item">
            <div>
              <h3>System Feedback Loop</h3>
              <p>Automatically mark decisions for retraining when variance is high.</p>
            </div>
            <label className="toggle-switch">
              <input type="checkbox" defaultChecked />
              <span className="slider round"></span>
            </label>
          </div>
        </div>
      </div>

      <div className="settings-actions">
        <button className="btn-primary" onClick={handleSave}>Save Preferences</button>
      </div>
    </div>
  );
};

export default SettingsPage;
