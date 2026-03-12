import React, { useState } from 'react';
import { ShieldCheck, ShieldAlert, Activity, BarChart2, Volume2, VolumeX } from 'lucide-react';

const ResultCard = ({ result }) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  
  if (!result) return null;

  const isFake = result.label === 'FAKE';
  const color = isFake ? 'var(--danger)' : 'var(--success)';
  const labelText = isFake ? 'High Probability of Misinformation' : 'High Probability of Authenticity';
  const confidence = (result.confidence * 100).toFixed(1);
  const realProb = (result.real_prob * 100).toFixed(1);
  const fakeProb = (result.fake_prob * 100).toFixed(1);

  const handleListen = () => {
    if ('speechSynthesis' in window) {
      if (isSpeaking) {
        window.speechSynthesis.cancel();
        setIsSpeaking(false);
        return;
      }
      
      const text = `The verdict for this content is ${result.label}. ${labelText}. Confidence score is ${confidence} percent.`;
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.onend = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
      setIsSpeaking(true);
    } else {
      alert("Text-to-speech is not supported in this browser.");
    }
  };

  return (
    <div className={`card fade-in ${isFake ? 'verdict-fake' : 'verdict-real'}`} style={{ borderLeftWidth: '6px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            {isFake ? <ShieldAlert size={24} /> : <ShieldCheck size={24} />}
            <span style={{ fontWeight: '800', fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Final Verdict
            </span>
          </div>
          <h2 style={{ fontSize: '2.5rem', fontWeight: '800', color: 'inherit', marginBottom: '4px' }}>
            {result.label}
          </h2>
          <p style={{ fontWeight: '500', opacity: 0.9 }}>{labelText}</p>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', alignItems: 'flex-end' }}>
          <div style={{ padding: '12px 16px', backgroundColor: 'white', borderRadius: '12px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', textAlign: 'center', minWidth: '100px' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: '800', color }}>{confidence}%</div>
            <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Confidence</div>
          </div>
          
          <button 
            onClick={handleListen}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '20px',
              border: '1px solid var(--border)',
              backgroundColor: 'white',
              cursor: 'pointer',
              fontSize: '0.75rem',
              fontWeight: '600',
              color: 'var(--text-muted)',
              transition: 'all 0.2s'
            }}
          >
            {isSpeaking ? <VolumeX size={14} /> : <Volume2 size={14} />}
            {isSpeaking ? 'Stop Listening' : 'Listen Verdict'}
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', fontWeight: '600', marginBottom: '4px', color: 'var(--text-main)' }}>
            <span>Authentic</span>
            <span>{realProb}%</span>
          </div>
          <div className="progress-bar-container">
            <div className="progress-bar" style={{ width: `${realProb}%`, backgroundColor: 'var(--success)' }} />
          </div>
        </div>
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', fontWeight: '600', marginBottom: '4px', color: 'var(--text-main)' }}>
            <span>Fake</span>
            <span>{fakeProb}%</span>
          </div>
          <div className="progress-bar-container">
            <div className="progress-bar" style={{ width: `${fakeProb}%`, backgroundColor: 'var(--danger)' }} />
          </div>
        </div>
      </div>

      <div style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid rgba(0,0,0,0.05)', display: 'flex', flexWrap: 'wrap', gap: '16px', fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <Activity size={14} /> Pipeline: {result.model_used || 'TF-IDF + Logistic Regression'}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <BarChart2 size={14} /> analysis: Statistical & NLP Processing
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
