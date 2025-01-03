import React from "react";
import { UserCircle2, Bot } from "lucide-react";

interface MessageProps {
  text: string;
  type: "user" | "assistant";
  timestamp: Date;
}

export function Message({ text, type, timestamp }: MessageProps) {
  const isUser = type === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="flex-shrink-0">
          <Bot className="h-8 w-8 text-blue-600" />
        </div>
      )}
      <div className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={`max-w-[80%] rounded-lg p-4 ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-white border border-gray-200 text-gray-800"
          }`}
          style={{ whiteSpace: "pre-wrap", lineHeight: "1.5" }}
        >
          {text}
        </div>
        <span className="text-xs text-gray-500 mt-1">
          {timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>
      {isUser && (
        <div className="flex-shrink-0">
          <UserCircle2 className="h-8 w-8 text-blue-600" />
        </div>
      )}
    </div>
  );
}
