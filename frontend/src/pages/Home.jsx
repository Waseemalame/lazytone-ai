import React, { useEffect, useState, useRef } from "react";
import api from "../api";
import "../styles/MessageCenter.css";
import AudioRecorder from "../components/AudioRecorder";
import ChatBox from "../components/ChatBox";

function Home() {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        fetchMessages();
    }, []);

    useEffect(() => {
        console.log(messages)
    }, [messages])

    const fetchMessages = async () => {
        try {
            const response = await api.get('/api/messages/');
            setMessages(response.data); // Assuming the API returns an array of messages
        } catch (error) {
            console.error('Failed to fetch messages:', error);
        }
    };

    return (
        <>
        <div className="home-container">
            <ChatBox messages={messages} />
            <AudioRecorder onNewMessage={fetchMessages} />
        </div>
        </>
    );
}

export default Home;
