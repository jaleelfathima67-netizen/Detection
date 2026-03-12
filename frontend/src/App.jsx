import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import InputArea from './components/InputArea';
import ResultCard from './components/ResultCard';
import { AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const resultRef = useRef(null);

  useEffect(() => {
    if (result && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [result]);

  const handleAnalyze = async (input, algorithm = 'logistic_regression') => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/detect/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input, model: algorithm }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Server error occurred during analysis.');
      }
    } catch (err) {
      setError('Could not connect to the backend. Please ensure the server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <Header />
      
      <motion.main 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <InputArea onAnalyze={handleAnalyze} loading={loading} />
        
        <AnimatePresence>
          {error && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="card" 
              style={{ borderColor: 'var(--danger)', display: 'flex', gap: '12px', alignItems: 'center', backgroundColor: '#fffcfc' }}
            >
              <AlertCircle color="var(--danger)" />
              <p style={{ color: 'var(--danger)', fontWeight: '500' }}>{error}</p>
            </motion.div>
          )}

          {result && (
            <motion.div 
              ref={resultRef}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <ResultCard result={result} />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.main>

      <footer style={{ marginTop: '40px', paddingBottom: '40px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
        <p>© 2026 Fake Buster AI · Intelligent Fake News Detection</p>
        <p style={{ marginTop: '8px', fontSize: '0.75rem', opacity: 0.7 }}>Powered by Scikit-Learn, NLTK & TF-IDF</p>
      </footer>
    </div>
  );
}

export default App;
