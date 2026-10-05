import type { PuzzleSubmissionResult } from "../api/types";

interface ResultBannerProps {
  result: PuzzleSubmissionResult | null;
  onDismiss: () => void;
}

export function ResultBanner({ result, onDismiss }: ResultBannerProps) {
  if (!result) return null;

  return (
    <div
      className={`fixed bottom-6 right-6 z-40 max-w-sm p-4 rounded border shadow-2xl animate-pulse-slow
        ${
          result.success
            ? "border-neon-green bg-bg-panel text-neon-green shadow-[0_0_20px_rgba(57,255,20,0.3)]"
            : "border-neon-pink bg-bg-panel text-neon-pink shadow-[0_0_20px_rgba(255,0,170,0.3)]"
        }`}
    >
      <div className="flex items-start gap-3">
        <span className="text-2xl">{result.success ? "✓" : "✗"}</span>
        <div className="flex-1">
          <p className="font-display font-bold uppercase text-sm">
            {result.success ? "Succès" : "Échec"}
          </p>
          <p className="text-xs text-slate-300 mt-1">{result.message}</p>
          {result.unlocked_door_id && (
            <p className="text-xs text-neon-cyan mt-1 font-mono">
              → Porte déverrouillée : {result.unlocked_door_id}
            </p>
          )}
        </div>
        <button
          onClick={onDismiss}
          className="text-slate-500 hover:text-slate-300"
          aria-label="Fermer"
        >
          ✕
        </button>
      </div>
    </div>
  );
}
