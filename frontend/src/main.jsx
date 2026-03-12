import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

console.log("main.jsx: Initializing React mount...");
const container = document.getElementById('root');
if (!container) {
  console.error("main.jsx: Root element '#root' not found in DOM!");
} else {
  console.log("main.jsx: Root found, rendering App...");
  createRoot(container).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}
