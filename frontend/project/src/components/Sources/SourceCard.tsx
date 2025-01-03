import React from "react";
import { Link2, BookOpen } from "lucide-react";

interface SourceCardProps {
  page_content: string;
  relevance: number;
  title: string;
  type: string;
}

export function SourceCard({
  page_content, // Page content as it is, we can show that on a tab on click after wards
  relevance,
  title,
  type,
}: SourceCardProps) {
  return (
    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:border-blue-200 transition-colors">
      <div className="flex items-start justify-between">
        <div className="flex gap-3">
          <BookOpen className="text-blue-600 flex-shrink-0" size={20} />
          <div>
            <h3 className="font-medium text-gray-800 overflow-hidden">
              {title}
            </h3>
            <p className="text-sm text-gray-600 mt-1">{type}</p>
            {/* <p className="text-xs text-gray-500 mt-1">Updated: {lastUpdated}</p> */}
            {/* <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1 mt-2"
            >
              <Link2 size={14} />
              View protocol
            </a> */}
          </div>
        </div>
        <span className="bg-blue-50 text-blue-700 text-xs font-medium px-2.5 py-1 rounded-full ">
          {relevance}
        </span>
      </div>
    </div>
  );
}
