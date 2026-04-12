import { api } from "../api/client";

const MOODS = [
  { value: 1, emoji: "😞", label: "Rough" },
  { value: 2, emoji: "😕", label: "Not great" },
  { value: 3, emoji: "😐", label: "Okay" },
  { value: 4, emoji: "🙂", label: "Good" },
  { value: 5, emoji: "😊", label: "Great" },
];

interface Props {
  userId: string;
  onLogged: () => void;
}

export function MoodCheckin({ userId, onLogged }: Props) {
  const handleMood = async (mood: number) => {
    await api.logMood(userId, mood);
    onLogged();
  };

  return (
    <div className="flex items-center gap-1">
      {MOODS.map((m) => (
        <button
          key={m.value}
          onClick={() => handleMood(m.value)}
          title={m.label}
          className="text-xl hover:scale-125 transition-transform p-1"
        >
          {m.emoji}
        </button>
      ))}
    </div>
  );
}
