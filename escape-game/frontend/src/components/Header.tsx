import { useEffect, useState } from "react";
import type { HealthStatus } from "../api/types";
import { api } from "../api/client";

export function Header() {
  const [health, setHealth] = useState<HealthStatus | null>(null);

  useEffect(() => {
    api.health().then(setHealth).catch(() => setHealth(null));
  }, []);

  return (
    <header className="border-b border-bg-border bg-bg-panel/60 backdrop-blur-md sticky top-0 z-20">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 relative">
            <div className="absolute inset-0 border-2 border-neon-cyan rotate-45" />
            <div className="absolute inset-2 bg-neon-pink rounded-full" />
          </div>
          <div>
            <h1 className="font-display font-black text-lg neon-text tracking-widest">
              OPERATION : NEON CYBERPUNK
            </h1>
            <p className="text-xs text-slate-500 uppercase tracking-widest">
              DigitalEscape Studio // Alpha Build
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs">
          {health ? (
            <>
              <span className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-neon-green animate-pulse" />
                <span className="text-neon-green uppercase">{health.status}</span>
              </span>
              <span className="text-slate-500">
                Engine{" "}
                <span className="text-neon-cyan font-bold">
                  v{health.engine_version}
                </span>
              </span>
              <span className="text-slate-500 hidden md:inline">
                Game Master :{" "}
                <span className="text-neon-pink">{health.game_master}</span>
              </span>
            </>
          ) : (
            <span className="text-red-500 uppercase">Hors ligne</span>
          )}
        </div>
      </div>
    </header>
  );
}
