import React from 'react';
import { SourceCard } from './SourceCard';
import { FileText } from 'lucide-react';

const sampleSources = [
  {
    title: "Clinical Practice Guidelines",
    url: "https://www.example.com/guidelines",
    relevance: 95,
    type: "Medical Protocol",
    lastUpdated: "2024-02-15"
  },
  {
    title: "Standard Operating Procedures",
    url: "https://www.example.com/sop",
    relevance: 88,
    type: "Procedure Manual",
    lastUpdated: "2024-02-10"
  }
];

export function SourcePanel() {
  return (
    <div className="h-full bg-gray-50">
      <div className="p-4 border-b border-gray-100 bg-white">
        <div className="flex items-center gap-2">
          <FileText className="text-blue-600" size={20} />
          <h2 className="text-lg font-semibold text-gray-900">Medical Sources</h2>
        </div>
        <p className="text-sm text-gray-600 mt-1">Evidence-based references and protocols</p>
      </div>
      
      <div className="p-6 space-y-4">
        {sampleSources.map((source, index) => (
          <SourceCard key={index} {...source} />
        ))}
      </div>
    </div>
  );
}