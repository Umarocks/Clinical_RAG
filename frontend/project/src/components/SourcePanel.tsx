import React from 'react';
import { Link2 } from 'lucide-react';

interface Source {
  title: string;
  url: string;
  relevance: number;
}

const sampleSources: Source[] = [
  {
    title: "Understanding React Hooks",
    url: "https://reactjs.org/docs/hooks-intro.html",
    relevance: 95
  },
  {
    title: "JavaScript Best Practices",
    url: "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
    relevance: 88
  },
];

export function SourcePanel() {
  return (
    <div className="h-full p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Sources</h2>
      <div className="space-y-4">
        {sampleSources.map((source, index) => (
          <div
            key={index}
            className="bg-white rounded-lg p-4 shadow-sm border border-gray-200"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-medium text-gray-900">{source.title}</h3>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1 mt-1"
                >
                  <Link2 size={14} />
                  View source
                </a>
              </div>
              <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">
                {source.relevance}% relevant
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}