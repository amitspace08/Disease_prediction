import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = ({ activePage }) => {
  const getAccentColor = () => {
    switch (activePage) {
      case 'Heart': return '#EF4444';
      case 'Liver': return '#22C55E';
      case 'Kidney':
      case 'Diabetes': return '#3B82F6';
      case 'About': return '#8B5CF6';
      default: return '#8B5CF6';
    }
  };

  return (
    <Container fluid className="px-0 mt-5">
      <hr style={{ borderColor: '#E2E8F0', margin: '3rem 0 1.5rem 0' }} />
      <div 
        className="d-flex flex-column align-items-center justify-content-center text-center pb-4" 
        style={{ gap: '0.5rem', color: '#64748B' }}
      >
        <div style={{ fontSize: '0.8rem' }}>
          MediPredict &copy; 2026 | Built for academic research and demonstration purposes.
        </div>
        <div style={{ fontSize: '0.75rem', maxWidth: '800px', lineHeight: 1.4 }}>
          <b>Disclaimer:</b> All analysis outputs are generated from statistical probabilities of clinical training sets and are completely advisory. Please seek official clinical testing and professional medical advice for definitive healthcare assessments.
        </div>
        <div style={{ fontSize: '0.8rem', fontWeight: 600, color: getAccentColor(), marginTop: '0.2rem' }}>
          Developed by Amit Kumar | National Institute of Technology Delhi
        </div>
      </div>
    </Container>
  );
};

export default Footer;
