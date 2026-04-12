import { Lock, Trash2 } from "lucide-react";
import type { Guideline } from "../api/client";

interface Props {
  guideline: Guideline;
  onDelete?: (id: string) => void;
  readOnly?: boolean;
}

export function GuidelineCard({ guideline, onDelete, readOnly }: Props) {
  return (
    <div className="flex items-start gap-3 py-3 border-b border-gray-100 last:border-0">
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          {guideline.is_safety && (
            <span className="inline-flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full">
              <Lock size={10} />
              Safety
            </span>
          )}
        </div>
        <p className="text-gray-700 mt-1 leading-relaxed">{guideline.guideline_text}</p>
        <p className="text-xs text-gray-400 mt-1">
          Added {new Date(guideline.created_at).toLocaleDateString()}
        </p>
      </div>
      {!readOnly && onDelete && (
        <button
          onClick={() => onDelete(guideline.id)}
          className="shrink-0 p-1.5 text-gray-300 hover:text-red-400 transition-colors"
          title="Remove"
        >
          <Trash2 size={16} />
        </button>
      )}
    </div>
  );
}
