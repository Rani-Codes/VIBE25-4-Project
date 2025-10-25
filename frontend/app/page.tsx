"use client";

import { useState } from "react";

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputText.trim()) return;
    
    setIsLoading(true);
    
    // Set the video URL from localhost:5000/video
    setVideoUrl("http://localhost:5000/video");
    
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-50 to-zinc-100 dark:from-zinc-950 dark:to-black">
      <div className="container mx-auto px-4 py-12 max-w-5xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-zinc-900 dark:text-zinc-50 mb-4">
            Video Generator
          </h1>
          <p className="text-lg text-zinc-600 dark:text-zinc-400">
            Enter your text to generate a video
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white dark:bg-zinc-900 rounded-2xl shadow-xl p-8 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label 
                htmlFor="textInput" 
                className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2"
              >
                Your Text
              </label>
              <textarea
                id="textInput"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Enter your text here..."
                rows={6}
                className="w-full px-4 py-3 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-all resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !inputText.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-400 dark:disabled:bg-zinc-700 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] disabled:cursor-not-allowed disabled:transform-none shadow-lg hover:shadow-xl"
            >
              {isLoading ? "Processing..." : "Generate Video"}
            </button>
          </form>
        </div>

        {/* Video Player */}
        {videoUrl && (
          <div className="bg-white dark:bg-zinc-900 rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-50 mb-6">
              Generated Video
            </h2>
            <div className="aspect-video w-full rounded-lg overflow-hidden bg-black">
              <video
                controls
                className="w-full h-full"
                src={videoUrl}
                poster=""
              >
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="mt-4 p-4 bg-zinc-50 dark:bg-zinc-800 rounded-lg">
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                <span className="font-medium">Video URL:</span>{" "}
                <a 
                  href={videoUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 dark:text-blue-400 hover:underline break-all"
                >
                  {videoUrl}
                </a>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
