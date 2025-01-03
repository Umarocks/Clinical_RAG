import React from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function ChatInput({ value, onChange, onSubmit }: ChatInputProps) {
  return (
    <form onSubmit={onSubmit} className="border-t border-gray-100 bg-white p-4">
      <div className="flex gap-2">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Ask about medical procedures or protocols..."
          className="flex-1 rounded-lg border border-gray-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white rounded-lg px-6 py-3 hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <span>Send</span>
          <Send size={18} />
        </button>
      </div>
    </form>
  );
}