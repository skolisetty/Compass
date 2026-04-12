import { ChevronDown, ChevronUp, Shield } from "lucide-react";
import { useState } from "react";
import type { Attribution } from "../api/client";

interface Props {
  role: "user" | "assistant";
  text: string;
  attributions?: Attribution[];
  loading?: boolean;
}

export function MessageBubble({ role, text, attributions, loading }: Props) {
  const [expanded, setExpanded] = useState(false);
  const isUser = role === "user";

  const uniqueVoices = attributions
    ? [...new Map(attributions.map((a) => [a.voice_name, a])).values()]
    : [];

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-teal-600 text-white rounded-br-md"
            : "bg-white border border-gray-200 text-gray-800 rounded-bl-md shadow-sm"
        }`}
      >
        {loading ? (
          <div className="flex items-center gap-2 text-gray-400">
            <div className="animate-pulse">Thinking with your Voices...</div>
          </div>
        ) : (
          <>
            <p className="whitespace-pre-wrap leading-relaxed">{text}</p>

            {!isUser && uniqueVoices.length > 0 && (
              <button
                onClick={() => setExpanded(!expanded)}
                className="mt-3 flex items-center gap-1.5 text-sm text-teal-600 hover:text-teal-700 transition-colors"
              >
                <Shield size={14} />
                <span>
                  Voice: {uniqueVoices.map((a) => `${a.voice_icon} ${a.voice_name}`).join(", ")}
                </span>
                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              </button>
            )}

            {expanded && attributions && (
              <div className="mt-2 border-t border-gray-100 pt-2 space-y-1.5">
                {attributions.map((a, i) => (
                  <div key={i} className="text-xs text-gray-500 flex items-start gap-1.5">
                    <span className="shrink-0">{a.voice_icon}</span>
                    <span>
                      <span className="font-medium text-gray-600">{a.voice_name}:</span>{" "}
                      "{a.guideline_text}"
                    </span>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
