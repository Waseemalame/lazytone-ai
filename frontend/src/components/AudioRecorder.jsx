/* eslint-disable react/prop-types */
import React, { useState, useEffect, useRef } from 'react';
import api from '../api';
import "../styles/MessageCenter.css"

const AudioRecorder = ({ onNewMessage }) => {
  const [messages, setMessages] = useState([
    { sender: 'VoiceBot', content: 'Hi, I am your AI VoiceBot, you can ask me anything.' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);
  useEffect(() => {
    listVoices()
  }, [])

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  function listVoices() {
    window.speechSynthesis.onvoiceschanged = () => {
        const voices = window.speechSynthesis.getVoices();
        console.log(voices);
        voices.forEach((voice, index) => console.log(index, voice.name, voice.lang));
    };
  }



  const saveMessage = async (text) => {
    try {
        const response = await api.post('/api/messages/', { text: text, sender_type: 'user' });
        console.log('Message saved:', response.data);
    } catch (error) {
        console.error('Failed to save message:', error);
    }
};

  const recordAndSend = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.start();
    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript;
      setInputText(transcript);
      recognition.stop();

      await saveMessage(transcript);
      onNewMessage();
      sendToOpenAI(transcript)
    };
  };

  const sendToOpenAI = async (text) => {
    api.post('/api/voicebot/', {message: text})
        .then(response => {
            // handle success
            console.log('Received response:', response.data.response);
            speak(response.data.response);
            onNewMessage();
        })
        .catch(error => {
            // handle error
            console.log(error);
        });
  };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    const allVoices = window.speechSynthesis.getVoices();
    const ziraVoice = allVoices.find(voice => voice.name.includes("Zira"));
    utterance.voice = ziraVoice;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };


  return (
          <button type="button" className="btn btn-primary btn-voice" onClick={recordAndSend} disabled={isSpeaking}>
            <i className="fa-solid fa-microphone"></i>
          </button>
    );
};

export default AudioRecorder;
