'use client';

import { useState } from 'react';

const CATEGORIES = [
  { name: 'Python', emoji: '🐍', color: 'bg-yellow-50 border-yellow-200', posts: 142, latestTitle: 'Best way to prepare for Python data structures?', replies: 23 },
  { name: 'React', emoji: '⚛️', color: 'bg-cyan-50 border-cyan-200', posts: 98, latestTitle: 'React hooks vs class components in interviews', replies: 18 },
  { name: 'Java', emoji: '☕', color: 'bg-orange-50 border-orange-200', posts: 87, latestTitle: 'Spring Boot microservices questions pattern', replies: 12 },
  { name: 'System Design', emoji: '🏗️', color: 'bg-blue-50 border-blue-200', posts: 76, latestTitle: 'How to approach URL shortener design?', replies: 31 },
  { name: 'DevOps', emoji: '🔧', color: 'bg-purple-50 border-purple-200', posts: 54, latestTitle: 'Kubernetes vs Docker Swarm comparison', replies: 9 },
  { name: 'iOS', emoji: '🍎', color: 'bg-gray-50 border-gray-200', posts: 43, latestTitle: 'SwiftUI interview tips for 2024', replies: 14 },
  { name: 'Android', emoji: '🤖', color: 'bg-green-50 border-green-200', posts: 39, latestTitle: 'Jetpack Compose state management', replies: 7 },
  { name: 'HR', emoji: '🤝', color: 'bg-pink-50 border-pink-200', posts: 65, latestTitle: 'How to answer "Tell me about yourself"', replies: 42 },
  { name: 'General', emoji: '💬', color: 'bg-slate-50 border-slate-200', posts: 210, latestTitle: 'Share your interview success stories!', replies: 56 },
];

const RECENT = [
  { author: 'Arjun P.', title: 'Tips for FAANG system design rounds', domain: 'System Design', time: '2h ago', replies: 8 },
  { author: 'Sneha R.', title: 'Python generator vs iterator explained', domain: 'Python', time: '4h ago', replies: 5 },
  { author: 'Vikram S.', title: 'My Google interview experience', domain: 'General', time: '6h ago', replies: 22 },
];

export default function ForumsPage() {
  const [showCreate, setShowCreate] = useState(false);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Forums</h1>
          <p className="text-gray-500 mt-1">Discuss interview strategies with the community.</p>
        </div>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="px-5 py-2.5 bg-blue-500 text-white text-sm font-semibold rounded-lg hover:bg-blue-600 transition-colors"
        >
          Create Post
        </button>
      </div>

      {/* Create Post Form */}
      {showCreate && (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">New Post</h2>
          <input placeholder="Post title..." className="w-full px-4 py-2.5 border border-gray-200 rounded-lg text-sm mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <textarea placeholder="Write your post..." rows={3} className="w-full px-4 py-2.5 border border-gray-200 rounded-lg text-sm mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <div className="flex gap-3">
            <select className="text-sm border border-gray-200 rounded-lg px-3 py-2">
              {CATEGORIES.map((c) => <option key={c.name}>{c.name}</option>)}
            </select>
            <button className="px-5 py-2 bg-blue-500 text-white text-sm font-semibold rounded-lg hover:bg-blue-600">Post</button>
          </div>
        </div>
      )}

      {/* Recent Discussions */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Trending Discussions</h2>
        <div className="space-y-3">
          {RECENT.map((r, i) => (
            <div key={i} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
              <div>
                <p className="text-sm font-medium text-gray-900">{r.title}</p>
                <p className="text-xs text-gray-400">{r.author} in {r.domain} &middot; {r.time}</p>
              </div>
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{r.replies} replies</span>
            </div>
          ))}
        </div>
      </div>

      {/* Domain Categories */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {CATEGORIES.map((cat) => (
          <div key={cat.name} className={`rounded-xl border p-5 hover:shadow-md transition-shadow cursor-pointer ${cat.color}`}>
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">{cat.emoji}</span>
              <div>
                <h3 className="font-semibold text-gray-900">{cat.name}</h3>
                <p className="text-xs text-gray-400">{cat.posts} posts</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 line-clamp-1">{cat.latestTitle}</p>
            <p className="text-xs text-gray-400 mt-1">{cat.replies} replies</p>
          </div>
        ))}
      </div>
    </div>
  );
}
