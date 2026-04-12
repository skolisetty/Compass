import { Activity, Send } from "lucide-react";
import { useCallback, useRef, useState } from "react";
import type { Attribution } from "../api/client";
import { api } from "../api/client";
import { MessageBubble } from "../components/MessageBubble";
import { MoodCheckin } from "../components/MoodCheckin";
import { WorkoutLogger } from "../components/WorkoutLogger";

interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  attributions?: Attribution[];
}

interface Props {
  userId: string;
  userName: string;
}

export function ChatPage({ userId, userName }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      text: `Hi ${userName}! How can I help you today?`,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showWorkout, setShowWorkout] = useState(false);
  const [moodLogged, setMoodLogged] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    setTimeout(() => messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }), 100);
  }, []);

  const handleSend = async () => {
    const q = input.trim();
    if (!q || loading) return;

    const userMsg: Message = { id: Date.now().toString(), role: "user", text: q };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    scrollToBottom();

    try {
      const res = await api.ask(userId, q);
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        text: res.answer,
        attributions: res.attributions,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          text: "Sorry, I had trouble responding. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-2xl mx-auto">
          {messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              role={msg.role}
              text={msg.text}
              attributions={msg.attributions}
            />
          ))}
          {loading && <MessageBubble role="assistant" text="" loading />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Workout Logger */}
      {showWorkout && (
        <div className="flex justify-center pb-2">
          <WorkoutLogger
            userId={userId}
            onClose={() => setShowWorkout(false)}
            onLogged={() => {
              setMessages((prev) => [
                ...prev,
                {
                  id: Date.now().toString(),
                  role: "assistant",
                  text: "Workout logged! 💪 I'll keep that in mind.",
                },
              ]);
            }}
          />
        </div>
      )}

      {/* Input area */}
      <div className="border-t border-gray-200 bg-white px-4 py-3">
        <div className="max-w-2xl mx-auto">
          {/* Mood row */}
          {!moodLogged && (
            <div className="flex items-center gap-2 mb-2 text-sm text-gray-400">
              <span>How are you feeling?</span>
              <MoodCheckin userId={userId} onLogged={() => setMoodLogged(true)} />
            </div>
          )}
          {moodLogged && (
            <div className="text-xs text-teal-500 mb-2">Mood logged ✓</div>
          )}

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowWorkout(!showWorkout)}
              className="shrink-0 p-2 rounded-lg text-gray-400 hover:text-teal-600 hover:bg-gray-50 transition-colors"
              title="Log a workout"
            >
              <Activity size={20} />
            </button>

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask anything..."
              className="flex-1 px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:border-teal-400 focus:ring-1 focus:ring-teal-400 text-gray-800 placeholder-gray-400"
              disabled={loading}
            />

            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="shrink-0 p-2.5 rounded-xl bg-teal-600 text-white hover:bg-teal-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
