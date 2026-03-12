import React from 'react';
import { ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

const Header = () => {
  return (
    <header style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      textAlign: 'center', 
      marginBottom: '60px' 
    }}>
      <motion.div 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
        style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '20px',
          marginBottom: '16px',
        }}
      >
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '8px',
          backgroundColor: 'rgba(255, 255, 255, 0.4)',
          padding: '8px 16px',
          borderRadius: '30px',
          backdropFilter: 'blur(8px)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          boxShadow: '0 4px 15px rgba(0, 0, 0, 0.05)'
        }}>
          <ShieldCheck size={20} color="var(--primary)" />
          <span style={{ fontSize: '0.875rem', fontWeight: '700', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
            AI-Powered Verification
          </span>
        </div>
        
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '6px',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          padding: '8px 16px',
          borderRadius: '30px',
          border: '1px solid rgba(16, 185, 129, 0.2)',
        }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--success)', animation: 'pulse 2s infinite' }}></div>
          <span style={{ fontSize: '0.75rem', fontWeight: '800', color: 'var(--success)', textTransform: 'uppercase' }}>
            System API: Online
          </span>
        </div>
      </motion.div>

      <motion.h1 
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        style={{ 
          fontSize: '3.5rem', 
          fontWeight: '800', 
          letterSpacing: '-0.04em',
          margin: '0 0 16px 0',
          lineHeight: '1.1',
          background: 'linear-gradient(135deg, #111827 0%, #4f46e5 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        Fake Buster <span style={{ color: 'var(--primary)', WebkitTextFillColor: 'var(--primary)' }}>AI</span>
      </motion.h1>
      
      <motion.p 
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        style={{ 
          color: 'var(--text-muted)', 
          fontSize: '1.25rem', 
          maxWidth: '580px', 
          margin: '0',
          fontWeight: '500',
          lineHeight: '1.6',
        }}
      >
        Intelligently detect misinformation and digital manipulation using advanced machine learning and NLP.
      </motion.p>
    </header>
  );
};

export default Header;

