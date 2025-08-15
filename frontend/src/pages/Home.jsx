import React, { useState, useEffect, useRef } from 'react';
import { sendMessage } from '../services/api';
import './Home.css'; // We'll create this file next for styling
import { ThumbsUp, ThumbsDown, Send } from 'lucide-react'; // Using icons for a cleaner look

export default function Home() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Function to automatically scroll to the latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = { text: input, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const botResponse = await sendMessage(input);
      const botMessage = {
        text: botResponse.reply || 'Sorry, I encountered an issue.',
        sender: 'bot',
        sources: botResponse.sources || [],
        sentiment: botResponse.sentiment || null,
        escalation: botResponse.escalation || null,
        feedback: null, // To track user feedback (like/dislike)
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { text: 'Failed to connect to the backend.', sender: 'bot' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = (index, feedbackType) => {
    // In a real app, you would send this feedback to your backend
    console.log(`Feedback for message ${index}: ${feedbackType}`);
    const updatedMessages = [...messages];
    updatedMessages[index].feedback = feedbackType;
    setMessages(updatedMessages);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Get the latest sentiment and escalation status from the last bot message
  const latestBotMessage = [...messages].reverse().find(msg => msg.sender === 'bot');
  const currentSentiment = latestBotMessage?.sentiment;
  const currentEscalation = latestBotMessage?.escalation;

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Customer Support AI</h2>
        <p>Powered by RAG and Sentiment Analysis</p>
      </div>

      {/* Status Panel to show real-time analysis */}
      <div className="status-panel">
        <div className="status-item">
          <strong>Sentiment:</strong>
          <span className={`sentiment-label ${currentSentiment?.label?.toLowerCase()}`}>
            {currentSentiment ? `${currentSentiment.label} (${(currentSentiment.score * 100).toFixed(0)}%)` : 'N/A'}
          </span>
        </div>
        <div className="status-item">
          <strong>Escalation Risk:</strong>
          <span className={`escalation-label ${currentEscalation?.prediction}`}>
            {currentEscalation ? `${currentEscalation.prediction.replace('_', ' ')}` : 'N/A'}
          </span>
        </div>
      </div>

      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message-wrapper ${msg.sender}`}>
            <div className="message-bubble">
              <p className="message-text">{msg.text}</p>
              {msg.sender === 'bot' && msg.sources.length > 0 && (
                <div className="sources-container">
                  <h4>Related Articles:</h4>
                  {msg.sources.map((source) => (
                    <div key={source.id} className="source-item">
                      <strong>{source.title}</strong>
                      <p>{source.snippet}</p>
                    </div>
                  ))}
                </div>
              )}
              {msg.sender === 'bot' && (
                <div className="feedback-container">
                  <button
                    onClick={() => handleFeedback(index, 'like')}
                    className={`feedback-btn like ${msg.feedback === 'like' ? 'selected' : ''}`}
                    disabled={msg.feedback}
                  >
                    <ThumbsUp size={16} />
                  </button>
                  <button
                    onClick={() => handleFeedback(index, 'dislike')}
                    className={`feedback-btn dislike ${msg.feedback === 'dislike' ? 'selected' : ''}`}
                    disabled={msg.feedback}
                  >
                    <ThumbsDown size={16} />
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper bot">
            <div className="message-bubble typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Describe your issue here..."
          rows="1"
        />
        <button onClick={handleSend} disabled={isLoading || !input.trim()}>
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}
