import React, { useState } from "react";
import { sendMessage } from "../services/api";

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { text: input, sender: "user" }]);
    setInput("");

    const botResponse = await sendMessage(input);
    setMessages((prev) => [...prev, { text: botResponse.response || botResponse.error, sender: "bot" }]);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>NerveSpark Chat</h1>
      <div style={{ border: "1px solid #ccc", padding: "10px", height: "300px", overflowY: "auto" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
            <p><b>{msg.sender}:</b> {msg.text}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        style={{ width: "80%", padding: "8px" }}
      />
      <button onClick={handleSend} style={{ padding: "8px" }}>Send</button>
    </div>
  );
}
