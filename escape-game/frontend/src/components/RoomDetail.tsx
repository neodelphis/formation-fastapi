import type { Room } from "../api/types";
import { Card, SectionTitle } from "./Card";

interface RoomDetailProps {
  room: Room;
  onPickupItem: (itemId: string) => void;
  onSolvePuzzle: (puzzleId: string) => void;
  inventory: string[];
}

export function RoomDetail({
  room,
  onPickupItem,
  onSolvePuzzle,
  inventory,
}: RoomDetailProps) {
  return (
    <div className="space-y-4">
      {/* Header de la salle */}
      <Card glow>
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h3 className="font-display font-black text-xl neon-text uppercase tracking-wider">
                {room.name}
              </h3>
              {room.is_start && (
                <span className="badge border-neon-green/50 text-neon-green">
                  Start
                </span>
              )}
              {room.is_exit && (
                <span className="badge border-neon-pink/50 text-neon-pink">
                  Exit
                </span>
              )}
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              {room.description}
            </p>
          </div>
          <code className="text-xs text-slate-600 font-mono">#{room.id}</code>
        </div>
      </Card>

      {/* Items */}
      {room.items.length > 0 && (
        <Card>
          <SectionTitle
            title="Objets présents"
            subtitle="Examinez ou ramassez les objets de la salle"
            icon="◇"
          />
          <div className="grid gap-2 sm:grid-cols-2">
            {room.items.map((item) => {
              const inInventory = inventory.includes(item.id);
              return (
                <div
                  key={item.id}
                  className="p-3 rounded border border-bg-border bg-bg-dark/40"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-sm text-slate-200">
                      {item.name}
                    </span>
                    {item.usable && (
                      <span className="badge border-neon-yellow/40 text-neon-yellow">
                        usable
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-500 mt-1">{item.description}</p>
                  <button
                    disabled={inInventory}
                    onClick={() => onPickupItem(item.id)}
                    className={`mt-2 w-full text-xs py-1 rounded border transition-all
                      ${
                        inInventory
                          ? "border-bg-border text-slate-600 cursor-not-allowed"
                          : "border-neon-green/50 text-neon-green hover:bg-neon-green/10"
                      }`}
                  >
                    {inInventory ? "✓ Dans l'inventaire" : "Ramasser"}
                  </button>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Doors */}
      {room.doors.length > 0 && (
        <Card>
          <SectionTitle title="Portes" icon="⌂" />
          <div className="space-y-2">
            {room.doors.map((door) => (
              <div
                key={door.id}
                className="flex items-center justify-between p-3 rounded border border-bg-border bg-bg-dark/40"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-200">
                      {door.name}
                    </span>
                    {door.is_locked ? (
                      <span className="badge border-neon-pink/50 text-neon-pink">
                        🔒 Verrouillée
                      </span>
                    ) : (
                      <span className="badge border-neon-green/50 text-neon-green">
                        🔓 Ouverte
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    {door.description}
                  </p>
                </div>
                {door.target_room_id && (
                  <code className="text-xs text-slate-600">
                    → {door.target_room_id}
                  </code>
                )}
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Puzzles */}
      {room.puzzles.length > 0 && (
        <Card>
          <SectionTitle
            title="Énigmes"
            subtitle="Tentez de résoudre les puzzles pour progresser"
            icon="▣"
          />
          <div className="space-y-3">
            {room.puzzles.map((puzzle) => (
              <div
                key={puzzle.id}
                className="p-4 rounded border border-neon-purple/30 bg-neon-purple/5"
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="font-display font-bold text-sm text-neon-purple uppercase tracking-wider">
                    {puzzle.name}
                  </span>
                  {puzzle.puzzle_kind && (
                    <span className="badge border-neon-purple/40 text-neon-purple">
                      {puzzle.puzzle_kind}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-400 mb-3">
                  {puzzle.description}
                </p>
                <button
                  onClick={() => onSolvePuzzle(puzzle.id)}
                  className="btn-cyber-pink w-full"
                >
                  Tenter une solution
                </button>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
