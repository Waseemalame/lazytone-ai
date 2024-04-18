/* eslint-disable react/prop-types */
import React from 'react';
import "../styles/MessageCenter.css"

const ChatBox = ({ messages }) => {
  return (
      <div className="chat-container">
          <div className="card flex-grow-1">
              <div className="card-header bg-primary text-white">Your lazy chat with Lazy Tone AI</div>
              <div className="card-body messages-box">
                  <ul className="list-unstyled messages-list">
                      {messages.map((msg, index) => (
                          <li key={index} className="message received">
                              <div className={msg.sender_type === 'ai' ? "ai-message-text" : "message-text"}>
                                  <div className="message-sender">
                                      <b>{msg.sender_type === 'ai' ? 'Lazybot' : 'You'}</b>
                                  </div>
                                  <div className="message-content">{msg.text}</div>
                              </div>
                          </li>
                      ))}
                  </ul>
              </div>
              <br/><br/><br/><br/><br/>
          </div>
      </div>
  );
};

export default ChatBox;
