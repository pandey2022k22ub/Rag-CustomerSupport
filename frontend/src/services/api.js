import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // Backend URL

export const sendMessage = async (text) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat/respond`, { text });
    return response.data;
  } catch (error) {
    console.error("Error sending message:", error);
    return { error: "Failed to connect to backend" };
  }
};
