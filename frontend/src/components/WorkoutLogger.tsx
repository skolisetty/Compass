import { Bike, Dumbbell, Footprints, X } from "lucide-react";
import { useState } from "react";
import { api } from "../api/client";

const ACTIVITIES = [
  { type: "run", icon: Footprints, label: "Run", emoji: "🏃" },
  { type: "walk", icon: Footprints, label: "Walk", emoji: "🚶" },
  { type: "cycle", icon: Bike, label: "Cycle", emoji: "🚴" },
  { type: "gym", icon: Dumbbell, label: "Gym", emoji: "💪" },
];

interface Props {
  userId: string;
  onClose: () => void;
  onLogged: () => void;
}

export function WorkoutLogger({ userId, onClose, onLogged }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const [duration, setDuration] = useState(30);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    if (!selected) return;
    setSaving(true);
    await api.logWorkout(userId, {
      activity_type: selected,
      duration_minutes: duration,
    });
    setSaving(false);
    onLogged();
    onClose();
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-4 w-80">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-800">Log a Workout</h3>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
          <X size={18} />
        </button>
      </div>

      <div className="grid grid-cols-4 gap-2 mb-4">
        {ACTIVITIES.map((a) => (
          <button
            key={a.type}
            onClick={() => setSelected(a.type)}
            className={`flex flex-col items-center gap-1 p-3 rounded-lg border-2 transition-colors ${
              selected === a.type
                ? "border-teal-500 bg-teal-50"
                : "border-gray-100 hover:border-gray-200"
            }`}
          >
            <span className="text-2xl">{a.emoji}</span>
            <span className="text-xs text-gray-600">{a.label}</span>
          </button>
        ))}
      </div>

      <div className="mb-4">
        <label className="text-sm text-gray-500 mb-1 block">Duration</label>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setDuration(Math.max(5, duration - 5))}
            className="w-8 h-8 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 font-bold"
          >
            -
          </button>
          <span className="text-lg font-semibold text-gray-800 w-16 text-center">
            {duration} min
          </span>
          <button
            onClick={() => setDuration(duration + 5)}
            className="w-8 h-8 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 font-bold"
          >
            +
          </button>
        </div>
      </div>

      <button
        onClick={handleSave}
        disabled={!selected || saving}
        className="w-full py-2 rounded-lg bg-teal-600 text-white font-medium hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {saving ? "Saving..." : "Log Workout"}
      </button>
    </div>
  );
}
