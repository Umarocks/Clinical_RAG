import React from 'react';
import { Stethoscope } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-white border-b border-blue-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Stethoscope className="text-blue-700" size={28} />
            <div>
              <h1 className="text-xl font-semibold text-gray-900">Medical Protocol Assistant</h1>
              <p className="text-sm text-gray-600">Evidence-based clinical guidance</p>
            </div>
          </div>
          <div className="text-sm text-gray-500">
            Last updated: {new Date().toLocaleDateString()}
          </div>
        </div>
      </div>
    </header>
  );
}