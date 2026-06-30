import React, { useState } from 'react';
import { Landmark, Info, Search, ArrowRight, Loader2, CheckCircle2, Clock, FileText, MessageSquare, List } from 'lucide-react';

const Header = ({ onReset, onToggleFunds, showFunds, showNewChat }) => (
  <header className="header">
    <div className="header-logo" onClick={onReset} style={{cursor: 'pointer'}}>
      <Landmark size={24} />
      <span>ZeroAdvice</span>
    </div>
    <div className="header-actions">
      {showNewChat && (
        <button className="nav-btn" onClick={onReset}>
          <MessageSquare size={18} />
          <span className="hide-mobile">New Chat</span>
        </button>
      )}
      <button className="nav-btn" onClick={onToggleFunds}>
        <List size={18} />
        <span className="hide-mobile">{showFunds ? 'Back to Chat' : 'Supported Funds'}</span>
      </button>
    </div>
  </header>
);

const Footer = () => (
  <footer className="footer">
    <div className="footer-logo">
      <Landmark size={18} />
      <span>ZeroAdvice</span>
    </div>
    <div className="footer-links">
      <span>Privacy Policy</span>
      <span>Terms of Service</span>
      <span>© 2026 ZeroAdvice. All rights reserved.</span>
    </div>
  </footer>
);

const DisclaimerBanner = () => (
  <div className="disclaimer-banner-wrapper">
    <div className="disclaimer-badge">
      <Info size={16} />
      <span>Facts-only. No investment advice.</span>
    </div>
  </div>
);

const WelcomeHero = () => (
  <div className="welcome-hero">
    <h1 className="welcome-title">Welcome to ZeroAdvice</h1>
  </div>
);

const SupportedFunds = () => {
  const [funds, setFunds] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const CACHE_KEY = 'zeroadvice_funds';
    const MAX_AGE_MS = 24 * 60 * 60 * 1000; // 1 day

    try {
      const cached = sessionStorage.getItem(CACHE_KEY);
      if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        if (Date.now() - timestamp < MAX_AGE_MS) {
          setFunds(data);
          setLoading(false);
          return;
        }
      }
    } catch (e) { /* ignore parse errors */ }

    fetch('/api/funds')
      .then(res => res.json())
      .then(data => {
        const fundsList = data.funds || [];
        setFunds(fundsList);
        sessionStorage.setItem(CACHE_KEY, JSON.stringify({ data: fundsList, timestamp: Date.now() }));
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="funds-view">
      <h2 className="funds-title">Supported Funds</h2>
      <p className="funds-subtitle">You can ask factual questions about the following mutual funds.</p>
      
      {loading ? (
        <div style={{display: 'flex', justifyContent: 'center', padding: '2rem'}}>
          <Loader2 className="spinner" size={32} />
        </div>
      ) : (
        <div className="funds-list">
          {funds.map((f, i) => (
            <div key={i} className="fund-item">
              <div className="fund-icon"><Landmark size={20} /></div>
              <div className="fund-details">
                <div className="fund-name">{f.name}</div>
                <div className="fund-type">{f.type}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const SuggestionChips = ({ onSelect }) => {
  const suggestions = [
    "What is the expense ratio of ICICI Prudential Large Cap Fund?",
    "Who manages the HDFC Flexi Cap Fund?",
    "What is the exit load if I redeem ICICI Prudential Flexicap Fund early?",
  ];

  return (
    <div className="suggestions-section">
      <div className="suggestions-label">Try asking about:</div>
      <div className="suggestions-list">
        {suggestions.map((s, i) => (
          <button key={i} className="suggestion-chip" onClick={() => onSelect(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
};

const SearchBar = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
      setQuery("");
    }
  };

  return (
    <div className="search-wrapper">
      <div className="search-container">
        <form className="search-form" onSubmit={handleSubmit}>
          <Search className="search-icon" size={20} />
          <input 
            type="text" 
            className="search-input" 
            placeholder="What are the average management fees for an index fund"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" className="search-button" disabled={!query.trim() || isLoading}>
            {isLoading ? <Loader2 className="spinner" size={20} /> : <ArrowRight size={20} />}
          </button>
        </form>
      </div>
    </div>
  );
};

const ResultFeed = ({ messages, bottomRef }) => {
  if (messages.length === 0) return null;

  return (
    <div className="results-feed">
      {messages.map((msg, idx) => {
        if (msg.role === 'user') {
          return (
            <div key={idx} className="message-user">
              {msg.text}
            </div>
          );
        }

        const res = msg.data;
        if (res.type === 'factual') {
          return (
            <div key={idx} className="message-assistant result-card factual-card">
              <div className="factual-header">
                <div className="icon-wrapper">
                  <CheckCircle2 size={24} />
                </div>
                <div>
                  <h3 className="factual-title">{res.title || "Factual Information"}</h3>
                </div>
              </div>
              <div className="factual-content">
                {res.answer}
              </div>
              <div className="factual-footer">
                <div className="footer-meta">
                  <Clock size={14} />
                  <span>Last updated: {res.last_updated ? res.last_updated.split('T')[0] : 'Unknown'}</span>
                </div>
                <a href={res.source_url} target="_blank" rel="noreferrer" className="footer-link">
                  <FileText size={14} />
                  <span>View Source</span>
                </a>
              </div>
            </div>
          );
        } else if (res.type === 'refusal') {
          return (
            <div key={idx} className="message-assistant result-card refusal-card">
              <Info className="refusal-icon" size={20} />
              <div className="refusal-content">
                <div className="refusal-title">Advisory Notice</div>
                <div className="refusal-text">
                  {res.answer}
                </div>
                {res.educational_link && (
                  <a href={res.educational_link} target="_blank" rel="noreferrer" style={{color: 'var(--warning-text)', fontWeight: 500, fontSize: '0.9rem', marginTop: '0.5rem', textDecoration: 'underline'}}>
                    Educational Link
                  </a>
                )}
              </div>
            </div>
          );
        }
        return null;
      })}
      <div ref={bottomRef} />
    </div>
  );
};

export default function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showFunds, setShowFunds] = useState(false);
  const [activeFundContext, setActiveFundContext] = useState(null);
  const bottomRef = React.useRef(null);

  const scrollToBottom = () => {
    if (!showFunds) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages, showFunds]);

  const handleReset = () => {
    setMessages([]);
    setShowFunds(false);
    setActiveFundContext(null);
  };

  const handleToggleFunds = () => {
    setShowFunds(!showFunds);
  };

  const handleSearch = async (query) => {
    const userMsg = { role: 'user', text: query };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: query, context_fund: activeFundContext })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        if (data.context_fund) {
          setActiveFundContext(data.context_fund);
        }
        setMessages((prev) => [...prev, { role: 'assistant', data }]);
      } else {
        setMessages((prev) => [...prev, { role: 'assistant', data: { type: 'refusal', answer: data.detail || "An error occurred." } }]);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', data: { type: 'refusal', answer: "Network error. Make sure the backend is running." } }]);
    } finally {
      setIsLoading(false);
    }
  };

  const showNewChat = messages.length > 0 && !showFunds;

  return (
    <div className="app-container">
      <Header onReset={handleReset} onToggleFunds={handleToggleFunds} showFunds={showFunds} showNewChat={showNewChat} />
      <DisclaimerBanner />
      
      {showFunds ? (
        <main className="main-content">
          <SupportedFunds />
        </main>
      ) : (
        <>
          <main className="main-content">
            {messages.length === 0 && <WelcomeHero />}
            {messages.length === 0 && <SuggestionChips onSelect={handleSearch} />}
            <ResultFeed messages={messages} bottomRef={bottomRef} />
          </main>
          <SearchBar onSubmit={handleSearch} isLoading={isLoading} />
        </>
      )}
    </div>
  );
}
