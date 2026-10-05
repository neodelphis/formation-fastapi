import { useEffect, useState } from "react";

interface PuzzleModalProps {
  open: boolean;
  puzzleName: string;
  puzzleKind: string | null;
  onClose: () => void;
  onSubmit: (code: string) => Promise<{ success: boolean; message: string }>;
}

export function PuzzleModal({
  open,
  puzzleName,
  puzzleKind,
  onClose,
  onSubmit,
}: PuzzleModalProps) {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{
    success: boolean;
    message: string;
  } | null>(null);

  useEffect(() => {
    if (open) {
      setCode("");
      setResult(null);
      setLoading(false);
    }
  }, [open]);

  if (!open) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const r = await onSubmit(code);
      setResult(r);
    } catch (err) {
      setResult({
        success: false,
        message: err instanceof Error ? err.message : "Erreur inconnue",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-bg-dark/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="panel-glow w-full max-w-md p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-display font-black text-lg neon-text-pink uppercase">
              {puzzleName}
            </h3>
            {puzzleKind && (
              <p className="text-xs text-slate-500 uppercase mt-1">
                Type : {puzzleKind}
                {puzzleKind === "hash" && " (SHA-256)"}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-neon-pink text-xl leading-none"
            aria-label="Fermer"
          >
            ✕
          </button>
        </div>

        {!result && (
          <form onSubmit={handleSubmit} className="space-y-3">
            <label className="block text-xs uppercase text-slate-400 tracking-wider">
              Votre tentative
            </label>
            <input
              autoFocus
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Saisissez le code / mot de passe..."
              className="input-cyber"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !code.trim()}
              className="btn-cyber-pink w-full disabled:opacity-50"
            >
              {loading ? "Vérification..." : "Soumettre"}
            </button>
            <p className="text-xs text-slate-600">
              ⚠ Un code vide sera rejeté par l'API (HTTP 422 Pydantic).
            </p>
          </form>
        )}

        {result && (
          <div className="space-y-4">
            <div
              className={`p-4 rounded border ${
                result.success
                  ? "border-neon-green/50 bg-neon-green/10"
                  : "border-neon-pink/50 bg-neon-pink/10"
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <span
                  className={`text-2xl ${
                    result.success ? "text-neon-green" : "text-neon-pink"
                  }`}
                >
                  {result.success ? "✓" : "✗"}
                </span>
                <span
                  className={`font-display font-bold uppercase ${
                    result.success ? "text-neon-green" : "text-neon-pink"
                  }`}
                >
                  {result.success ? "Succès" : "Échec"}
                </span>
              </div>
              <p className="text-sm text-slate-300">{result.message}</p>
            </div>
            <button onClick={onClose} className="btn-cyber w-full">
              Fermer
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
