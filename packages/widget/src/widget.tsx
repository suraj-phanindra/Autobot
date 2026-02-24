import { useState, useRef, useEffect, useCallback } from 'react'
import { widgetApi, type QueryResponse } from './api/client'

interface Message {
  id: string
  role: 'user' | 'bot'
  content: string
  timestamp: Date
  vehicles?: QueryResponse['vehicles']
}

interface WidgetProps {
  config: {
    apiKey: string
    apiUrl: string
    primaryColor?: string
    greeting?: string
    position?: string
  }
}

export function Widget({ config }: WidgetProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'greeting',
      role: 'bot',
      content: config.greeting || 'Hi! Ask me anything about our vehicles.',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => crypto.randomUUID())
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const api = widgetApi(config.apiUrl, config.apiKey)

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, scrollToBottom])

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus()
    }
  }, [isOpen])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || isLoading) return

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await api.query(text, sessionId)
      const botMessage: Message = {
        id: crypto.randomUUID(),
        role: 'bot',
        content: response.answer,
        timestamp: new Date(),
        vehicles: response.vehicles,
      }
      setMessages(prev => [...prev, botMessage])
    } catch {
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      {isOpen && (
        <div className="autobot-panel">
          <div className="autobot-header">
            <h3>AutoBot</h3>
            <button onClick={() => setIsOpen(false)} aria-label="Close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <div className="autobot-messages">
            {messages.map(msg => (
              <div key={msg.id} className={`autobot-message autobot-message--${msg.role}`}>
                {msg.content}
              </div>
            ))}
            {isLoading && (
              <div className="autobot-message autobot-message--loading">
                <div className="autobot-typing">
                  <span /><span /><span />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="autobot-input-area">
            <input
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about our vehicles..."
              disabled={isLoading}
            />
            <button onClick={handleSend} disabled={isLoading || !input.trim()}>
              Send
            </button>
          </div>

          <div className="autobot-powered">
            Powered by <a href="https://autobot.ai" target="_blank" rel="noopener">AutoBot</a>
          </div>
        </div>
      )}

      <button
        className="autobot-fab"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        )}
      </button>
    </>
  )
}
