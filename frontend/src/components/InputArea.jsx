import { useState } from 'react';
import { FileText, Search, RotateCcw, Quote, Activity, BarChart2, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

const InputArea = ({ onAnalyze, loading }) => {
  const [text, setText] = useState('');
  const [selectedModel, setSelectedModel] = useState('logistic_regression');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) onAnalyze(text, selectedModel);
  };

  const handleClear = () => setText('');

  const canSubmit = !loading && text.trim().length > 0;

  return (
    <div className="card" style={{ padding: '28px 30px' }}>

      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        marginBottom: '20px',
        paddingBottom: '16px',
        borderBottom: '1px solid #f1f5f9'
      }}>
        <div style={{
          width: '36px', height: '36px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 4px 12px rgba(99,102,241,0.25)'
        }}>
          <FileText size={18} color="white" />
        </div>
        <div>
          <div style={{ fontWeight: '800', fontSize: '1rem', color: 'var(--text-main)', lineHeight: 1.2 }}>
            Analyze News Content
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: '500' }}>
            Headline · Article · Social media snippet
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Textarea */}
        <div style={{ position: 'relative' }}>
          <textarea
            className="textarea"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste a news headline, article snippet, or social media post here to check if it's real or fake..."
            style={{
              minHeight: '130px',
              maxHeight: '220px',
              padding: '16px 20px',
              fontSize: '0.95rem',
              lineHeight: '1.65',
              resize: 'vertical',
              paddingRight: '50px'
            }}
          />
          <Quote
            size={36}
            style={{
              position: 'absolute',
              bottom: '16px',
              right: '16px',
              opacity: 0.06,
              pointerEvents: 'none',
              transform: 'rotate(180deg)'
            }}
          />
        </div>

        {/* Quick Test Cases */}
        <div style={{ marginTop: '18px' }}>
          <div style={{
            fontSize: '0.68rem',
            fontWeight: '800',
            color: 'var(--text-muted)',
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            marginBottom: '10px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <div style={{ width: '10px', height: '2px', backgroundColor: 'var(--primary)', borderRadius: '2px' }}></div>
            Quick Test Cases
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '7px' }}>
            {[
              { label: 'Politics',      emoji: '🏛️', text: 'G7 leaders meet in Brussels to discuss global energy policy and security.',              bg: 'linear-gradient(135deg,#dbeafe,#bfdbfe)', color: '#1e40af', border: '#93c5fd' },
              { label: 'Health',        emoji: '🩺', text: 'New medical breakthrough helps treat common heart conditions.',                         bg: 'linear-gradient(135deg,#dcfce7,#bbf7d0)', color: '#166534', border: '#86efac' },
              { label: 'Science',       emoji: '🔬', text: 'NASA confirms discovery of liquid water on Mars surface.',                              bg: 'linear-gradient(135deg,#ede9fe,#ddd6fe)', color: '#5b21b6', border: '#c4b5fd' },
              { label: 'Tech',          emoji: '💻', text: 'SpaceX Starship successfully completes orbital flight test mission.',                   bg: 'linear-gradient(135deg,#e0f2fe,#bae6fd)', color: '#0c4a6e', border: '#7dd3fc' },
              { label: '⚠ Fake Health', emoji: '🧪', text: 'Drinking bleach can cure any disease instantly according to secret experts.',          bg: 'linear-gradient(135deg,#fff7ed,#fed7aa)', color: '#9a3412', border: '#fdba74' },
              { label: '⚠ Conspiracy',  emoji: '🛸', text: 'Secret satellites are using space lasers to control the weather globally.',            bg: 'linear-gradient(135deg,#fef2f2,#fecaca)', color: '#991b1b', border: '#fca5a5' },
            ].map((ex, idx) => (
              <motion.button
                key={idx}
                type="button"
                onClick={() => setText(ex.text)}
                whileHover={{ scale: 1.06, y: -2 }}
                whileTap={{ scale: 0.97 }}
                style={{
                  fontSize: '0.76rem',
                  padding: '6px 12px',
                  borderRadius: '20px',
                  border: `1.5px solid ${ex.border}`,
                  background: ex.bg,
                  color: ex.color,
                  fontWeight: '700',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.06)',
                  transition: 'all 0.2s'
                }}
              >
                <span style={{ fontSize: '0.85rem' }}>{ex.emoji}</span>
                {ex.label}
              </motion.button>
            ))}
          </div>
        </div>

        {/* Algorithm Selector */}
        <div style={{ marginTop: '20px' }}>
          <div style={{
            fontSize: '0.68rem',
            fontWeight: '800',
            color: 'var(--text-muted)',
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            marginBottom: '10px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <div style={{ width: '10px', height: '2px', backgroundColor: 'var(--secondary)', borderRadius: '2px' }}></div>
            Analysis Algorithm
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(145px, 1fr))', gap: '8px' }}>
            {[
              { id: 'logistic_regression', name: 'Logistic Regression', desc: 'Fast & Balanced',   icon: <Activity size={14} /> },
              { id: 'naive_bayes',         name: 'Naive Bayes',         desc: 'Text Optimized',    icon: <BarChart2 size={14} /> },
              { id: 'svm',                 name: 'SVM',                 desc: 'High Precision',    icon: <ShieldCheck size={14} /> },
              { id: 'random_forest',       name: 'Random Forest',       desc: 'Ensemble Robust',   icon: <Activity size={14} /> },
            ].map((m) => (
              <div
                key={m.id}
                onClick={() => setSelectedModel(m.id)}
                onMouseEnter={(e) => {
                  if (selectedModel !== m.id) {
                    e.currentTarget.style.borderColor = '#93c5fd';
                    e.currentTarget.style.backgroundColor = '#eff6ff';
                    e.currentTarget.style.boxShadow = '0 4px 14px rgba(59,130,246,0.18)';
                    e.currentTarget.querySelector('.algo-icon-label').style.color = '#1d4ed8';
                  }
                }}
                onMouseLeave={(e) => {
                  if (selectedModel !== m.id) {
                    e.currentTarget.style.borderColor = 'rgba(0,0,0,0.08)';
                    e.currentTarget.style.backgroundColor = 'white';
                    e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.04)';
                    e.currentTarget.querySelector('.algo-icon-label').style.color = 'var(--text-main)';
                  }
                }}
                style={{
                  padding: '10px 12px',
                  borderRadius: '12px',
                  border: '1.5px solid',
                  borderColor: selectedModel === m.id ? 'var(--primary)' : 'rgba(0,0,0,0.08)',
                  backgroundColor: selectedModel === m.id ? 'var(--primary-light)' : 'white',
                  cursor: 'pointer',
                  transition: 'border-color 0.2s, background-color 0.2s, box-shadow 0.2s',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '3px',
                  boxShadow: selectedModel === m.id ? '0 4px 12px rgba(79,70,229,0.15)' : '0 1px 3px rgba(0,0,0,0.04)'
                }}
              >
                <div
                  className="algo-icon-label"
                  style={{ display: 'flex', alignItems: 'center', gap: '5px', color: selectedModel === m.id ? 'var(--primary)' : 'var(--text-main)', transition: 'color 0.2s' }}
                >
                  {m.icon}
                  <span style={{ fontSize: '0.8rem', fontWeight: '700' }}>{m.name}</span>
                </div>
                <span style={{ fontSize: '0.66rem', color: 'var(--text-muted)', paddingLeft: '19px' }}>{m.desc}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Action Row */}
        <div style={{
          display: 'flex',
          justifyContent: 'flex-end',
          gap: '10px',
          marginTop: '20px',
          borderTop: '1px solid #f1f5f9',
          paddingTop: '16px',
          alignItems: 'center'
        }}>
          {/* char count */}
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginRight: 'auto' }}>
            {text.length} characters
          </span>

          {/* Reset */}
          <motion.button
            type="button"
            onClick={handleClear}
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
            style={{
              display: 'flex', alignItems: 'center', gap: '6px',
              padding: '9px 18px',
              borderRadius: '10px',
              border: '1.5px solid #e2e8f0',
              backgroundColor: 'white',
              color: 'var(--text-muted)',
              fontWeight: '700',
              fontSize: '0.85rem',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
            onMouseOver={(e) => { e.currentTarget.style.borderColor = 'var(--primary)'; e.currentTarget.style.color = 'var(--primary)'; }}
            onMouseOut={(e)  => { e.currentTarget.style.borderColor = '#e2e8f0';        e.currentTarget.style.color = 'var(--text-muted)'; }}
          >
            <RotateCcw size={14} />
            Reset
          </motion.button>

          {/* Run Detection */}
          <motion.button
            type="submit"
            disabled={!canSubmit}
            whileHover={canSubmit ? { scale: 1.03, boxShadow: '0 8px 28px rgba(99,102,241,0.45)' } : {}}
            whileTap={canSubmit ? { scale: 0.97 } : {}}
            style={{
              display: 'flex', alignItems: 'center', gap: '8px',
              padding: '10px 26px',
              borderRadius: '10px',
              border: 'none',
              background: canSubmit
                ? 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 55%, #a855f7 100%)'
                : 'linear-gradient(135deg, #c7c7e2, #a5b4fc)',
              color: 'white',
              fontWeight: '800',
              fontSize: '0.9rem',
              cursor: canSubmit ? 'pointer' : 'not-allowed',
              letterSpacing: '0.02em',
              boxShadow: canSubmit ? '0 4px 16px rgba(99,102,241,0.3)' : 'none',
              minWidth: '150px',
              justifyContent: 'center',
              transition: 'all 0.25s'
            }}
          >
            {loading ? (
              <>
                <div className="spinner" style={{ marginRight: '2px' }} />
                Analyzing...
              </>
            ) : (
              <>
                <Search size={16} strokeWidth={2.5} />
                Run Detection
              </>
            )}
          </motion.button>
        </div>
      </form>
    </div>
  );
};

export default InputArea;
