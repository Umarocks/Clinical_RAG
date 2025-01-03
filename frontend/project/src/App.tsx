import React from "react";
import { Header } from "./components/Header/Header";
import { ChatBox } from "./components/Chat/ChatBox";
import { SourcePanel } from "./components/Sources/SourcePanel";
import { useState } from "react";

interface Source {
  page_content?: string;
  page_number?: number;
  source?: string;
}

function App() {
  const [sharedData, setSharedData] = useState<Source[] | null>(null);
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-8rem)]">
          <div className="lg:col-span-2 bg-white rounded-lg shadow-sm overflow-hidden">
            <ChatBox setSharedData={setSharedData} />
          </div>
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <SourcePanel sharedData={sharedData} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
