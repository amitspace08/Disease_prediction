import React from 'react';
import { Button } from 'react-bootstrap';
import { FaHome, FaHeart, FaFlask, FaRegFileAlt, FaHistory, FaUserCircle, FaCog, FaShieldAlt, FaTint } from 'react-icons/fa';
import { GiKidneys } from 'react-icons/gi';

const Sidebar = ({ activePage, setActivePage, triggerToast }) => {
  const getSidebarItemStyle = (id) => {
    const isActive = activePage === id;
    
    if (isActive) {
      switch (id) {
        case 'Heart':
          return { backgroundColor: '#EF4444', color: '#FFFFFF', fontWeight: 700 };
        case 'Liver':
          return { backgroundColor: '#22C55E', color: '#FFFFFF', fontWeight: 700 };
        case 'Kidney':
        case 'Diabetes':
          return { backgroundColor: '#3B82F6', color: '#FFFFFF', fontWeight: 700 };
        case 'History':
          return { backgroundColor: '#6366F1', color: '#FFFFFF', fontWeight: 700 };
        case 'Home':
          return { backgroundColor: 'rgba(255, 255, 255, 0.08)', color: '#EF4444', borderLeft: '3px solid #EF4444', fontWeight: 700 };
        default:
          return { backgroundColor: 'rgba(255, 255, 255, 0.08)', color: '#FFFFFF', fontWeight: 700 };
      }
    }
    
    return {
      backgroundColor: 'transparent',
      color: '#8E8E93',
      borderLeft: '3px solid transparent'
    };
  };

  return (
    <div 
      className="position-fixed top-0 bottom-0 start-0 d-flex flex-column p-3" 
      style={{
        width: '260px',
        backgroundColor: '#0B0B0E',
        borderRight: '1px solid #1A1A22',
        paddingTop: '5.5rem',
        zIndex: 99,
        overflowY: 'auto'
      }}
    >
      {/* Title Header */}
      <div className="pb-2 mb-3" style={{ borderBottom: '1px solid #222227' }}>
        <span style={{ fontWeight: 800, fontSize: '1.15rem', color: '#EF4444', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span className="animate-pulse">🩺</span> Smart Health Assistant
        </span>
        <div style={{ fontSize: '0.78rem', color: '#8E8E93', marginTop: '0.2rem' }}>Your health, predicted by AI</div>
      </div>

      {/* Main Menu */}
      <div className="mb-4">
        <div style={{ fontSize: '0.7rem', fontWeight: 700, color: '#52525B', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '0.6rem' }}>
          MAIN MENU
        </div>
        <div 
          className="d-flex align-items-center px-3 py-2 rounded" 
          style={{ ...getSidebarItemStyle('Home'), cursor: 'pointer', transition: 'all 0.2s ease', fontSize: '0.9rem' }}
          onClick={() => setActivePage('Home')}
        >
          <FaHome className="me-2" />
          <span>Dashboard</span>
        </div>
      </div>

      {/* Disease Predictions */}
      <div className="mb-4">
        <div style={{ fontSize: '0.7rem', fontWeight: 700, color: '#52525B', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '0.6rem' }}>
          DISEASE PREDICTIONS
        </div>
        
        <div className="d-flex flex-column gap-1">
          <div 
            className="d-flex align-items-center px-3 py-2 rounded" 
            style={{ ...getSidebarItemStyle('Heart'), cursor: 'pointer', transition: 'all 0.2s ease', fontSize: '0.9rem' }}
            onClick={() => setActivePage('Heart')}
          >
            <FaHeart className="me-2" />
            <span>Heart Disease</span>
          </div>

          <div 
            className="d-flex align-items-center px-3 py-2 rounded" 
            style={{ ...getSidebarItemStyle('Liver'), cursor: 'pointer', transition: 'all 0.2s ease', fontSize: '0.9rem' }}
            onClick={() => setActivePage('Liver')}
          >
            <FaFlask className="me-2" />
            <span>Liver Disease</span>
          </div>

          <div 
            className="d-flex align-items-center px-3 py-2 rounded" 
            style={{ ...getSidebarItemStyle('Kidney'), cursor: 'pointer', transition: 'all 0.2s ease', fontSize: '0.9rem' }}
            onClick={() => setActivePage('Kidney')}
          >
            <GiKidneys className="me-2" />
            <span>Kidney Disease</span>
          </div>

          <div 
            className="d-flex align-items-center px-3 py-2 rounded" 
            style={{ ...getSidebarItemStyle('Diabetes'), cursor: 'pointer', transition: 'all 0.2s ease', fontSize: '0.9rem' }}
            onClick={() => setActivePage('Diabetes')}
          >
            <FaTint className="me-2" />
            <span>Diabetes</span>
          </div>
        </div>
      </div>

      {/* Tools & History */}
      <div className="mb-4">
        <div style={{ fontSize: '0.7rem', fontWeight: 700, color: '#52525B', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '0.6rem' }}>
          TOOLS & HISTORY
        </div>
        <div className="d-flex flex-column gap-1" style={{ color: '#8E8E93' }}>
          <div 
            className="d-flex align-items-center px-3 py-2 rounded" 
            style={{ ...getSidebarItemStyle('History'), cursor: 'pointer', transition: 'all 0.2s ease', fontSize: '0.9rem' }}
            onClick={() => setActivePage('History')}
          >
            <FaRegFileAlt className="me-2" />
            <span>Health Records</span>
          </div>
        </div>
      </div>

      {/* Spacer */}
      <div className="flex-grow-1"></div>

      {/* Need Help? Card */}
      <div className="help-card mb-3">
        <h6>Need Help?</h6>
        <p>Talk to our AI assistant for personalized health insights.</p>
        <Button 
          variant="outline-danger" 
          size="sm" 
          className="w-100" 
          style={{ fontSize: '0.8rem', fontWeight: 600 }}
          onClick={() => triggerToast("AI Medical Assistant coming soon! 🤖")}
        >
          Ask AI Assistant
        </Button>
      </div>

      {/* Secure Info Footer */}
      <div 
        className="d-flex align-items-center justify-content-center text-center px-1" 
        style={{ fontSize: '0.72rem', color: '#71717A', gap: '0.3rem' }}
      >
        <FaShieldAlt />
        <span>Your data is secure & confidential</span>
      </div>
    </div>
  );
};

export default Sidebar;
