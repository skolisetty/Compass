import { Compass, Eye, MessageCircle, Mic2 } from "lucide-react";
import { useState } from "react";
import { ChatPage } from "./pages/ChatPage";
import { OverviewPage } from "./pages/OverviewPage";
import { VoicePage } from "./pages/VoicePage";

type Page = "chat" | "overview" | "voices";

const PERSONAS = [
  { id: "margaret", name: "Margaret", emoji: "👵", desc: "74, independent elder" },
  { id: "david", name: "David", emoji: "🚴", desc: "35, fitness enthusiast" },
  { id: "sam", name: "Sam", emoji: "🧒", desc: "8, 3rd grader" },
] as const;

export default function App() {
  const [page, setPage] = useState<Page>("chat");
  const [userId, setUserId] = useState("margaret");

  const persona = PERSONAS.find((p) => p.id === userId)!;

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-2.5 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2.5">
          <Compass size={24} className="text-teal-600" />
          <span className="font-bold text-lg text-gray-800">Compass</span>
        </div>

        {/* Persona switcher */}
        <div className="flex items-center gap-1 bg-gray-100 rounded-full p-0.5">
          {PERSONAS.map((p) => (
            <button
              key={p.id}
              onClick={() => setUserId(p.id)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                userId === p.id
                  ? "bg-white text-gray-800 shadow-sm"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              <span>{p.emoji}</span>
              <span>{p.name}</span>
            </button>
          ))}
        </div>
      </header>

      {/* Navigation tabs */}
      <nav className="bg-white border-b border-gray-100 px-4 flex justify-center gap-1 shrink-0">
        {[
          { key: "chat" as const, label: "Chat", icon: MessageCircle },
          { key: "overview" as const, label: "My Compass", icon: Eye },
          { key: "voices" as const, label: "Voices", icon: Mic2 },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setPage(tab.key)}
            className={`flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
              page === tab.key
                ? "border-teal-600 text-teal-600"
                : "border-transparent text-gray-400 hover:text-gray-600"
            }`}
          >
            <tab.icon size={16} />
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Page content */}
      <main className="flex-1 overflow-hidden">
        {page === "chat" && (
          <ChatPage userId={userId} userName={persona.name} />
        )}
        {page === "overview" && <OverviewPage userId={userId} />}
        {page === "voices" && <VoicePage userId={userId} />}
      </main>
    </div>
  );
}
