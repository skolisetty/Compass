import { Plus } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import type { Guideline, Voice } from "../api/client";
import { api } from "../api/client";
import { GuidelineCard } from "../components/GuidelineCard";

interface Props {
  userId: string;
}

export function VoicePage({ userId }: Props) {
  const [voices, setVoices] = useState<Voice[]>([]);
  const [selectedVoice, setSelectedVoice] = useState<Voice | null>(null);
  const [guidelines, setGuidelines] = useState<Guideline[]>([]);
  const [newText, setNewText] = useState("");
  const [isSafety, setIsSafety] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    const v = await api.getVoices(userId);
    setVoices(v);
    if (v.length > 0 && !selectedVoice) {
      setSelectedVoice(v[0]);
    }
  }, [userId, selectedVoice]);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    if (!selectedVoice) return;
    api.getGuidelines(userId, selectedVoice.id).then(setGuidelines);
  }, [userId, selectedVoice]);

  const handleAdd = async () => {
    if (!newText.trim() || !selectedVoice) return;
    setSubmitting(true);
    await api.createGuideline(userId, selectedVoice.id, {
      guideline_text: newText.trim(),
      domain: selectedVoice.domains.split(",")[0],
      is_safety: isSafety,
    });
    setNewText("");
    setIsSafety(false);
    const updated = await api.getGuidelines(userId, selectedVoice.id);
    setGuidelines(updated);
    setSubmitting(false);
  };

  const handleDelete = async (id: string) => {
    await api.deleteGuideline(id);
    setGuidelines((prev) => prev.filter((g) => g.id !== id));
  };

  if (!selectedVoice) return null;

  const userLabel =
    userId === "margaret" ? "Margaret" : userId === "david" ? "David" : "Sam";

  const promptText: Record<string, string> = {
    doctor: `What should Compass know when helping ${userLabel} with health or medications?`,
    caregiver: `What should Compass know about ${userLabel}'s daily routines and care?`,
    coach: `What training or nutrition guidance should Compass follow for ${userLabel}?`,
    family: `What should Compass know about ${userLabel}'s home life and routines?`,
    teacher: `What should Compass know about ${userLabel} in the classroom?`,
    financial_advisor: `What financial guidance should Compass follow for ${userLabel}?`,
    therapist: `What should Compass know to support ${userLabel}'s mental wellbeing?`,
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-1">
        Voice Guidance for {userLabel}
      </h1>
      <p className="text-gray-400 text-sm mb-6">
        Add guidance that shapes how Compass helps them.
      </p>

      {/* Voice selector */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {voices.map((v) => (
          <button
            key={v.id}
            onClick={() => setSelectedVoice(v)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              selectedVoice.id === v.id
                ? "bg-teal-600 text-white"
                : "bg-white text-gray-600 border border-gray-200 hover:border-teal-300"
            }`}
          >
            <span>{v.icon}</span>
            <span>{v.name}</span>
          </button>
        ))}
      </div>

      {/* Selected voice header */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5 mb-6">
        <div className="flex items-center gap-3 mb-3">
          <span className="text-3xl">{selectedVoice.icon}</span>
          <div>
            <h2 className="font-semibold text-gray-800">{selectedVoice.name}</h2>
            <p className="text-sm text-gray-400">
              {selectedVoice.role.charAt(0).toUpperCase() + selectedVoice.role.slice(1)} ·{" "}
              {selectedVoice.domains.split(",").join(", ")}
            </p>
          </div>
        </div>

        <p className="text-sm text-gray-500 mb-3">
          {promptText[selectedVoice.role] || "What guidance should Compass follow?"}
        </p>

        <div className="flex gap-2">
          <input
            type="text"
            value={newText}
            onChange={(e) => setNewText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAdd()}
            placeholder="Type your guidance..."
            className="flex-1 px-4 py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:border-teal-400 focus:ring-1 focus:ring-teal-400 text-sm"
            disabled={submitting}
          />
          <button
            onClick={handleAdd}
            disabled={!newText.trim() || submitting}
            className="px-4 py-2.5 rounded-lg bg-teal-600 text-white text-sm font-medium hover:bg-teal-700 disabled:opacity-40 transition-colors flex items-center gap-1"
          >
            <Plus size={16} />
            Add
          </button>
        </div>

        <label className="flex items-center gap-2 mt-2 text-xs text-gray-400 cursor-pointer">
          <input
            type="checkbox"
            checked={isSafety}
            onChange={(e) => setIsSafety(e.target.checked)}
            className="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
          />
          This is a safety rule (cannot be overridden)
        </label>
      </div>

      {/* Guidelines list */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
        <h3 className="font-semibold text-gray-800 mb-3">
          Active Guidance ({guidelines.length})
        </h3>
        {guidelines.length === 0 ? (
          <p className="text-gray-400 text-sm py-4 text-center">
            No guidance added yet. Start by typing above.
          </p>
        ) : (
          guidelines.map((g) => (
            <GuidelineCard key={g.id} guideline={g} onDelete={handleDelete} />
          ))
        )}
      </div>
    </div>
  );
}
