import { Lock, Settings } from "lucide-react";
import { useEffect, useState } from "react";
import type { GuidanceOverview } from "../api/client";
import { api } from "../api/client";

interface Props {
  userId: string;
}

export function OverviewPage({ userId }: Props) {
  const [overview, setOverview] = useState<GuidanceOverview | null>(null);

  useEffect(() => {
    api.getOverview(userId).then(setOverview);
  }, [userId]);

  if (!overview) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        Loading...
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-1">
        What Shapes Your Compass
      </h1>
      <p className="text-gray-400 text-sm mb-6">
        The people you trust guide how Compass helps you. Here's what everyone
        has shared.
      </p>

      {/* Voice sections */}
      {overview.voices.map(({ voice, guidelines }) => (
        <div
          key={voice.id}
          className="bg-white rounded-xl border border-gray-200 shadow-sm p-5 mb-4"
        >
          <div className="flex items-center gap-3 mb-3">
            <span className="text-2xl">{voice.icon}</span>
            <div>
              <h2 className="font-semibold text-gray-800">{voice.name}</h2>
              <p className="text-sm text-gray-400">
                {voice.role.charAt(0).toUpperCase() + voice.role.slice(1)} ·{" "}
                {voice.domains.split(",").join(", ")}
              </p>
            </div>
          </div>

          <div className="space-y-2">
            {guidelines.map((g) => (
              <div key={g.id} className="flex items-start gap-2">
                {g.is_safety ? (
                  <Lock size={14} className="text-amber-500 mt-0.5 shrink-0" />
                ) : (
                  <span className="text-gray-300 mt-0.5 shrink-0">·</span>
                )}
                <p className="text-gray-700 text-sm leading-relaxed">
                  {g.guideline_text}
                </p>
              </div>
            ))}
            {guidelines.length === 0 && (
              <p className="text-gray-400 text-sm italic">
                No guidance added yet.
              </p>
            )}
          </div>
        </div>
      ))}

      {/* Platform defaults */}
      {overview.platform_defaults.length > 0 && (
        <div className="rounded-xl border-2 border-dashed border-gray-200 p-5">
          <div className="flex items-center gap-2 mb-3">
            <Settings size={18} className="text-gray-400" />
            <div>
              <h2 className="font-semibold text-gray-600">Compass Defaults</h2>
              <p className="text-xs text-gray-400">Always active</p>
            </div>
          </div>
          <div className="space-y-2">
            {overview.platform_defaults.map((text, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="text-gray-300 mt-0.5 shrink-0">·</span>
                <p className="text-gray-500 text-sm">{text}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
