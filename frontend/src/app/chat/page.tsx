'use client';

import { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '@/lib/types';

const QUICK_ACTIONS = [
  'Explain closures in JavaScript',
  'Common system design patterns',
  'Python vs Java differences',
  'How to prepare for HR rounds',
];

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: '1',
    role: 'assistant',
    content: 'Hello! I\'m your AI interview coach. Ask me anything about interview preparation, technical concepts, or get tips for your upcoming interviews. What would you like to discuss?',
    timestamp: new Date().toISOString(),
  },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    // Simulate AI response (mock)
    setTimeout(() => {
      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: getMockResponse(text),
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1200);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-6 h-[calc(100vh-64px)] flex flex-col">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-gray-900">AI Interview Coach</h1>
        <p className="text-sm text-gray-500">Ask questions, get explanations, and practice concepts.</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white rounded-br-md'
                  : 'bg-slate-100 text-gray-800 rounded-bl-md'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-slate-100 px-4 py-3 rounded-2xl rounded-bl-md">
              <div className="flex gap-1.5">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="flex gap-2 mb-3 overflow-x-auto pb-1">
        {QUICK_ACTIONS.map((action) => (
          <button
            key={action}
            onClick={() => sendMessage(action)}
            className="flex-shrink-0 px-3 py-1.5 bg-white border border-gray-200 rounded-full text-xs font-medium text-gray-600 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-600 transition-colors"
          >
            {action}
          </button>
        ))}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 px-4 py-3 bg-slate-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-colors"
        />
        <button
          type="submit"
          disabled={!input.trim() || isTyping}
          className="px-5 py-3 bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </form>
    </div>
  );
}

function getMockResponse(input: string): string {
  const lower = input.toLowerCase();
  if (lower.includes('closure')) {
    return 'A closure is a function that retains access to variables from its outer (enclosing) scope even after the outer function has returned. In JavaScript, closures are created every time a function is created. They are commonly used for data privacy, callbacks, and creating factory functions.';
  }
  if (lower.includes('system design')) {
    return 'Key system design patterns include: (1) Load Balancing for distributing traffic, (2) Caching with Redis or Memcached, (3) Database Sharding for horizontal scaling, (4) Message Queues for async processing, (5) Microservices for modular architecture. Start with requirements gathering, then estimate scale, design the high-level architecture, and dive into components.';
  }
  if (lower.includes('python') && lower.includes('java')) {
    return 'Python is dynamically typed and interpreted, great for rapid prototyping and data science. Java is statically typed and compiled to bytecode, preferred for large-scale enterprise applications. Python has simpler syntax but Java offers better performance and stronger type safety. Both have extensive ecosystems and strong job markets.';
  }
  if (lower.includes('hr') || lower.includes('behavioral')) {
    return 'For HR/behavioral rounds, use the STAR method: Situation, Task, Action, Result. Prepare stories about leadership, conflict resolution, teamwork, and handling failure. Be authentic, quantify results when possible, and always show what you learned. Common questions cover strengths/weaknesses, career goals, and why you want this role.';
  }
  return 'That\'s a great question! In an interview setting, I\'d recommend structuring your answer clearly: start with a high-level overview, then dive into specifics, and finish with practical examples or trade-offs. Would you like me to help you practice answering this type of question?';
}
