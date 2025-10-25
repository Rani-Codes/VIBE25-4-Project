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

  const handleExampleVideo = (title: string, description: string, videoUrl: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      text: title,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate API delay
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        text: description,
        videoUrl: videoUrl,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 800);
  };

  const handleClearChat = () => {
    setMessages([]);
  };

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
    const currentPrompt = inputText;
    setInputText("");
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await fetch(
        `http://localhost:8000/prompt?prompt=${encodeURIComponent(currentPrompt)}`
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
    <div className="flex flex-col h-screen bg-black relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-[#ff2e63] rounded-full mix-blend-multiply filter blur-[128px] animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-[#ff6b35] rounded-full mix-blend-multiply filter blur-[128px] animate-pulse [animation-delay:1s]"></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-[#ffb800] rounded-full mix-blend-multiply filter blur-[128px] animate-pulse [animation-delay:2s]"></div>
      </div>

      {/* Header */}
      <div className="relative z-10 bg-zinc-950/50 backdrop-blur-xl border-b border-[#ff2e63]/20 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-linear-to-br from-[#ff2e63] to-[#ff6b35] flex items-center justify-center shadow-xl border border-white/10">
              <svg
                className="w-7 h-7 text-white"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-linear-to-r from-[#ff2e63] via-[#ff6b35] to-[#ffb800] bg-clip-text text-transparent tracking-tight">
                Smarty Pants
          </h1>
              <p className="text-xs text-zinc-400 font-mono tracking-wide">
                Video Generation Engine
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            {messages.length > 0 && (
              <button
                onClick={handleClearChat}
                className="px-3 py-1.5 text-xs font-semibold text-zinc-400 hover:text-[#ff2e63] hover:bg-zinc-900/50 border border-zinc-800 hover:border-[#ff2e63]/30 rounded-lg transition-all flex items-center gap-2"
              >
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Clear
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="relative z-10 flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-5xl mx-auto space-y-6">
          {messages.length === 0 && (
            <div className="text-center py-20 animate-in fade-in duration-500">
              <div className="relative inline-block mb-8">
                <div className="absolute inset-0 bg-linear-to-br from-[#ff2e63] to-[#ff6b35] rounded-3xl blur-xl animate-pulse"></div>
                <div className="relative w-24 h-24 rounded-3xl bg-linear-to-br from-[#ff2e63] to-[#ff6b35] flex items-center justify-center shadow-2xl border-2 border-white/20">
                  <svg
                    className="w-12 h-12 text-white"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </div>
              </div>
              <h3 className="text-4xl font-bold text-white mb-4 tracking-tight">
                Ready to Create
              </h3>
              <p className="text-zinc-400 mb-8 max-w-md mx-auto font-mono text-sm tracking-wide">
                Type your prompt below or try one of these examples
              </p>
              <div className="flex flex-wrap justify-center gap-4 max-w-3xl mx-auto">
                <button
                  onClick={() => handleExampleVideo(
                    "Show me vector addition",
                    "Here's an educational video explaining vector addition with visual examples.",
                    "http://127.0.0.1:8000/media/videos/vector_addition/480p15/VectorAddition.mp4"
                  )}
                  disabled={isLoading}
                  className="group relative px-6 py-4 bg-zinc-950/70 hover:bg-zinc-900/70 border-2 border-[#ff2e63]/30 hover:border-[#ff2e63] text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all disabled:opacity-50 flex flex-col items-center gap-2 min-w-[200px]"
                >
                  <svg className="w-6 h-6 text-[#ff2e63]" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  <span className="text-sm">Vector Addition</span>
                </button>

                <button
                  onClick={() => handleExampleVideo(
                    "Explain the quadratic equation",
                    "Here's a detailed explanation of the quadratic equation and how to solve it.",
                    "http://127.0.0.1:8000/media/videos/quadratic_manim/480p15/QuadraticEquation.mp4"
                  )}
                  disabled={isLoading}
                  className="group relative px-6 py-4 bg-zinc-950/70 hover:bg-zinc-900/70 border-2 border-[#ff6b35]/30 hover:border-[#ff6b35] text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all disabled:opacity-50 flex flex-col items-center gap-2 min-w-[200px]"
                >
                  <svg className="w-6 h-6 text-[#ff6b35]" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                  <span className="text-sm">Quadratic Equation</span>
                </button>

                <button
                  onClick={() => handleExampleVideo(
                    "Teach me integral calculus",
                    "Here's an introduction to integral calculus with step-by-step examples.",
                    "http://127.0.0.1:8000/media/videos/integral_calculus/480p15/IntegralCalculus.mp4"
                  )}
                  disabled={isLoading}
                  className="group relative px-6 py-4 bg-zinc-950/70 hover:bg-zinc-900/70 border-2 border-[#ffb800]/30 hover:border-[#ffb800] text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all disabled:opacity-50 flex flex-col items-center gap-2 min-w-[200px]"
                >
                  <svg className="w-6 h-6 text-[#ffb800]" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                  </svg>
                  <span className="text-sm">Integral Calculus</span>
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={message.id}
              className={`flex gap-3 animate-in fade-in slide-in-from-bottom-4 duration-500 ${
                message.type === "user" ? "justify-end" : "justify-start"
              }`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Assistant Avatar */}
              {message.type === "assistant" && (
                <div className="shrink-0 w-12 h-12 rounded-2xl bg-linear-to-br from-[#ff2e63] to-[#ff6b35] flex items-center justify-center shadow-xl border border-white/10">
                  <svg
                    className="w-6 h-6 text-white"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </div>
              )}

              <div
                className={`max-w-3xl ${
                  message.type === "user" ? "ml-12" : "mr-12"
                }`}
              >
                {/* User Message */}
                {message.type === "user" && (
                  <div className="bg-zinc-950/90 backdrop-blur-sm text-white rounded-2xl rounded-tr-md px-6 py-4 shadow-xl border border-[#ff6b35]/30 hover:border-[#ff6b35]/50 transition-all">
                    <p className="text-sm leading-relaxed font-medium">{message.text}</p>
                    <p className="text-xs text-[#ffb800] mt-2 font-mono tracking-wide">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                )}

                {/* Assistant Message */}
                {message.type === "assistant" && (
                  <div className="bg-zinc-950/70 backdrop-blur-sm rounded-2xl rounded-tl-md shadow-2xl hover:shadow-[#ff2e63]/20 transition-all overflow-hidden border border-zinc-800 hover:border-[#ff2e63]/30">
                    {message.text && (
                      <div className="px-6 py-4 border-b border-zinc-800/50">
                        <p className="text-sm text-zinc-300 leading-relaxed font-medium">
                          {message.text}
          </p>
        </div>
                    )}
                    {message.videoUrl && (
                      <div className="p-4">
                        <div className="relative aspect-video w-full rounded-xl overflow-hidden bg-black shadow-2xl border-2 border-[#ff2e63]/20">
                          <div className="absolute inset-0 bg-linear-to-br from-[#ff2e63]/10 to-transparent pointer-events-none"></div>
                          <video
                            controls
                            className="w-full h-full relative z-10"
                            src={message.videoUrl}
                            poster=""
                          >
                            Your browser does not support the video tag.
                          </video>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* User Avatar */}
              {message.type === "user" && (
                <div className="shrink-0 w-12 h-12 rounded-2xl bg-linear-to-br from-[#ffb800] to-[#ff6b35] flex items-center justify-center shadow-xl border border-white/10">
                  <svg
                    className="w-6 h-6 text-white"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2.5}
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 animate-in fade-in duration-300">
              <div className="shrink-0 w-12 h-12 rounded-2xl bg-linear-to-br from-[#ff2e63] to-[#ff6b35] flex items-center justify-center shadow-xl border border-white/10">
                <svg
                  className="w-6 h-6 text-white animate-spin"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
              <div className="max-w-3xl mr-12">
                <div className="bg-zinc-950/70 backdrop-blur-sm rounded-2xl rounded-tl-md px-6 py-4 shadow-xl border border-zinc-800">
                  <div className="flex items-center space-x-3">
                    <div className="w-3 h-3 bg-[#ff2e63] rounded-full animate-bounce"></div>
                    <div className="w-3 h-3 bg-[#ff6b35] rounded-full animate-bounce [animation-delay:0.2s]"></div>
                    <div className="w-3 h-3 bg-[#ffb800] rounded-full animate-bounce [animation-delay:0.4s]"></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="relative z-10 bg-zinc-950/50 backdrop-blur-xl border-t border-[#ff2e63]/20 px-4 py-5 shadow-2xl">
        <div className="max-w-5xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your prompt..."
                disabled={isLoading}
                className="w-full px-6 py-3.5 rounded-xl border-2 border-zinc-800 bg-zinc-950/80 text-white placeholder-zinc-600 focus:outline-none focus:ring-2 focus:ring-[#ff2e63] focus:border-[#ff2e63] disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg font-mono tracking-wide text-sm"
              />
              {inputText && (
                <button
                  type="button"
                  onClick={() => setInputText("")}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-zinc-600 hover:text-[#ff2e63] transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
            <button
              type="submit"
              disabled={isLoading || !inputText.trim()}
              className="group relative px-6 py-3.5 bg-linear-to-br from-[#ff2e63] to-[#ff6b35] hover:from-[#ff1744] hover:to-[#ff2e63] disabled:from-zinc-800 disabled:to-zinc-900 text-white font-bold rounded-xl transition-all duration-200 disabled:cursor-not-allowed shadow-lg disabled:shadow-none transform hover:scale-105 active:scale-95 disabled:transform-none flex items-center gap-2 border border-white/10"
            >
              {isLoading ? (
                <>
                  <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span className="hidden sm:inline text-sm">Processing</span>
                </>
              ) : (
                <>
                  <span className="hidden sm:inline text-sm">Generate</span>
                  <svg
                    className="w-4 h-4 group-hover:translate-x-1 transition-transform"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2.5}
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
