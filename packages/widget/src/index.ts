import { createElement } from 'react'
import { createRoot } from 'react-dom/client'
import { Widget } from './widget'

interface AutoBotConfig {
  apiKey: string
  apiUrl: string
  primaryColor?: string
  greeting?: string
  position?: 'bottom-right' | 'bottom-left'
}

function getConfig(): AutoBotConfig {
  const script = document.currentScript as HTMLScriptElement | null
  if (!script) {
    throw new Error('AutoBot: Could not find script element')
  }

  const apiKey = script.getAttribute('data-api-key')
  const apiUrl = script.getAttribute('data-api-url')

  if (!apiKey || !apiUrl) {
    throw new Error('AutoBot: data-api-key and data-api-url attributes are required')
  }

  return {
    apiKey,
    apiUrl,
    primaryColor: script.getAttribute('data-primary-color') || '#2563eb',
    greeting: script.getAttribute('data-greeting') || 'Hi! Ask me anything about our vehicles.',
    position: (script.getAttribute('data-position') as AutoBotConfig['position']) || 'bottom-right',
  }
}

function mount() {
  const config = getConfig()

  // Create host element
  const host = document.createElement('div')
  host.id = 'autobot-widget-host'
  document.body.appendChild(host)

  // Attach Shadow DOM for style isolation
  const shadow = host.attachShadow({ mode: 'open' })

  // Inject styles into shadow DOM
  const styleSheet = document.createElement('style')
  styleSheet.textContent = getWidgetStyles(config.primaryColor!, config.position!)
  shadow.appendChild(styleSheet)

  // Mount React app inside shadow DOM
  const mountPoint = document.createElement('div')
  mountPoint.id = 'autobot-widget-root'
  shadow.appendChild(mountPoint)

  const root = createRoot(mountPoint)
  root.render(createElement(Widget, { config }))
}

function getWidgetStyles(primaryColor: string, position: string): string {
  const positionStyles = position === 'bottom-left'
    ? 'left: 20px;'
    : 'right: 20px;'

  return `
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .autobot-fab {
      position: fixed;
      bottom: 20px;
      ${positionStyles}
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background-color: ${primaryColor};
      color: white;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      transition: transform 0.2s, box-shadow 0.2s;
      z-index: 999999;
    }

    .autobot-fab:hover {
      transform: scale(1.05);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    }

    .autobot-fab svg {
      width: 24px;
      height: 24px;
    }

    .autobot-panel {
      position: fixed;
      bottom: 88px;
      ${positionStyles}
      width: 380px;
      height: 520px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      z-index: 999998;
      animation: slideUp 0.3s ease-out;
    }

    @keyframes slideUp {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .autobot-header {
      padding: 16px;
      background-color: ${primaryColor};
      color: white;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .autobot-header h3 {
      font-size: 16px;
      font-weight: 600;
    }

    .autobot-header button {
      background: none;
      border: none;
      color: white;
      cursor: pointer;
      padding: 4px;
    }

    .autobot-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .autobot-message {
      max-width: 85%;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 14px;
      line-height: 1.5;
      word-wrap: break-word;
    }

    .autobot-message--bot {
      align-self: flex-start;
      background-color: #f1f5f9;
      color: #1e293b;
      border-bottom-left-radius: 4px;
    }

    .autobot-message--user {
      align-self: flex-end;
      background-color: ${primaryColor};
      color: white;
      border-bottom-right-radius: 4px;
    }

    .autobot-message--loading {
      align-self: flex-start;
      background-color: #f1f5f9;
      color: #94a3b8;
      border-bottom-left-radius: 4px;
    }

    .autobot-typing {
      display: flex;
      gap: 4px;
      padding: 4px 0;
    }

    .autobot-typing span {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: #94a3b8;
      animation: bounce 1.4s ease-in-out infinite;
    }

    .autobot-typing span:nth-child(2) { animation-delay: 0.2s; }
    .autobot-typing span:nth-child(3) { animation-delay: 0.4s; }

    @keyframes bounce {
      0%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-6px); }
    }

    .autobot-input-area {
      padding: 12px 16px;
      border-top: 1px solid #e2e8f0;
      display: flex;
      gap: 8px;
    }

    .autobot-input-area input {
      flex: 1;
      padding: 10px 12px;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }

    .autobot-input-area input:focus {
      border-color: ${primaryColor};
    }

    .autobot-input-area button {
      padding: 10px 16px;
      background-color: ${primaryColor};
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      transition: opacity 0.2s;
    }

    .autobot-input-area button:hover {
      opacity: 0.9;
    }

    .autobot-input-area button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .autobot-powered {
      padding: 6px;
      text-align: center;
      font-size: 11px;
      color: #94a3b8;
      background: #f8fafc;
    }

    .autobot-powered a {
      color: #64748b;
      text-decoration: none;
    }
  `
}

// Auto-mount when script loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mount)
} else {
  mount()
}
