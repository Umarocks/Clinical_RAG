import React, { useEffect, useState } from "react";
import { SourceCard } from "./SourceCard";
import { FileText } from "lucide-react";

export function SourcePanel({ sharedData }: any) {
  interface Source {
    title: string;
    page_content: string;
    relevance: number;
    type: string;
  }
  return (
    <div className="h-full bg-gray-50">
      <div className="p-4 border-b border-gray-100 bg-white">
        <div className="flex items-center gap-2">
          <FileText className="text-blue-600" size={20} />
          <h2 className="text-lg font-semibold text-gray-900">
            Medical Sources
          </h2>
        </div>
        <p className="text-sm text-gray-600 mt-1">
          Evidence-based references and protocols
        </p>
      </div>

      {sharedData?.map((source: Source, index: number) => (
        <SourceCard key={index} {...source} />
      ))}
    </div>
  );
}
