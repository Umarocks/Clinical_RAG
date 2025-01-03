import React, { useState } from "react";
import { Message } from "./Message";
import { ChatInput } from "./ChatInput";

interface ChatMessage {
  text: string;
  type: "user" | "assistant";
  timestamp: Date;
}
interface RequestData {
  query: string;
}

interface ResponseData {
  answer: string; // Adjust this based on the expected response structure
  error?: string; // If your API might return an error message
}
interface Source {
  page_content: string;
  page_number: number;
  source: string;
}
export function ChatBox({ setSharedData }: any) {
  const [response, setResponse] = useState<ResponseData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const fetchData = async () => {
    try {
      const requestData: RequestData = {
        query: input,
      };
      const res = await fetch("http://127.0.0.1:5000/ask_pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      let formatted = data.answer;
      // Replace **text** or *text* or ***text*** with <b>text</b>
      formatted = formatted.replace(/\*+([^*]+)\*+/g, "<b>$1</b>");
      setResponse({ answer: formatted });
      const sharedData = data.sources;
      setSharedData(sharedData);
      return response;
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred.");
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage: ChatMessage = {
      text: input,
      type: "user",
      timestamp: new Date(),
    };

    setMessages([...messages, newMessage]);
    // Simulate response

    await fetchData();
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          text: response?.answer || error || "I'm sorry, Some Error Occured.",
          type: "assistant",
          timestamp: new Date(),
        },
      ]);
    }, 4000);
    setInput("");
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      <div className="p-4 border-b border-gray-100 bg-white">
        <h2 className="text-lg font-semibold text-gray-900">
          Clinical Consultation
        </h2>
        <p className="text-sm text-gray-600">
          Ask questions about medical procedures and protocols
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((message, index) => (
          <Message
            key={index}
            text={message.text}
            type={message.type}
            timestamp={message.timestamp}
          />
        ))}
      </div>

      <ChatInput value={input} onChange={setInput} onSubmit={handleSubmit} />
    </div>
  );
}
