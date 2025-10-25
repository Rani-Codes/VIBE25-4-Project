"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  id: string;
  type: "user" | "assistant";
  text?: string;
  videoUrl?: string;
  timestamp: Date;
}

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      text: inputText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await fetch(
        `http://localhost:8000/prompt?prompt=${encodeURIComponent(inputText)}`
      );

      if (!response.ok) {
        throw new Error("Failed to generate video");
      }

      const data = await response.json();

      // Add assistant message with video
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        text: data.message,
        videoUrl: data.video_url,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        text: "Sorry, something went wrong. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-linear-to-br from-zinc-50 to-zinc-100 dark:from-zinc-950 dark:to-black">
      {/* Header */}
      <div className="bg-white dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 px-6 py-4 shadow-sm">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">
            Video Generator Chat
          </h1>
          <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-1">
            Chat with AI to generate videos from your prompts
          </p>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-5xl mx-auto space-y-6">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900/30 mb-4">
                <svg
                  className="w-8 h-8 text-blue-600 dark:text-blue-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
                Start a conversation
              </h3>
              <p className="text-zinc-600 dark:text-zinc-400">
                Send a message to generate your first video
              </p>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.type === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-3xl ${
                  message.type === "user" ? "ml-12" : "mr-12"
                }`}
              >
                {/* User Message */}
                {message.type === "user" && (
                  <div className="bg-blue-600 text-white rounded-2xl px-6 py-4 shadow-md">
                    <p className="text-sm leading-relaxed">{message.text}</p>
                  </div>
                )}

                {/* Assistant Message */}
                {message.type === "assistant" && (
                  <div className="bg-white dark:bg-zinc-900 rounded-2xl shadow-lg overflow-hidden">
                    {message.text && (
                      <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-800">
                        <p className="text-sm text-zinc-700 dark:text-zinc-300">
                          {message.text}
                        </p>
                      </div>
                    )}
                    {message.videoUrl && (
                      <div className="p-4">
                        <div className="aspect-video w-full rounded-lg overflow-hidden bg-black">
                          <video
                            controls
                            className="w-full h-full"
                            src={message.videoUrl}
                            poster=""
                          >
                            Your browser does not support the video tag.
                          </video>
                        </div>
                        <div className="mt-3 px-2">
                          <p className="text-xs text-zinc-500 dark:text-zinc-400">
                            <a
                              href={message.videoUrl}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="hover:text-blue-600 dark:hover:text-blue-400 hover:underline break-all"
                            >
                              {message.videoUrl}
                            </a>
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                <p className="text-xs text-zinc-500 dark:text-zinc-500 mt-2 px-2">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-3xl mr-12">
                <div className="bg-white dark:bg-zinc-900 rounded-2xl px-6 py-4 shadow-lg">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-zinc-400 dark:bg-zinc-600 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-zinc-400 dark:bg-zinc-600 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                    <div className="w-2 h-2 bg-zinc-400 dark:bg-zinc-600 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white dark:bg-zinc-900 border-t border-zinc-200 dark:border-zinc-800 px-4 py-4 shadow-lg">
        <div className="max-w-5xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 px-4 py-3 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            />
            <button
              type="submit"
              disabled={isLoading || !inputText.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-400 dark:disabled:bg-zinc-700 text-white font-semibold rounded-xl transition-all duration-200 disabled:cursor-not-allowed shadow-md hover:shadow-lg flex items-center gap-2"
            >
              <span>Send</span>
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
