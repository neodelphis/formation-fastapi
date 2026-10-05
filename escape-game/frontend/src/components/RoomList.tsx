import type { RoomSummary } from "../api/types";

interface RoomListProps {
  rooms: RoomSummary[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function RoomList({ rooms, selectedId, onSelect }: RoomListProps) {
  return (
    <div className="space-y-2">
      {rooms.map((room) => {
        const isActive = room.id === selectedId;
        return (
          <button
            key={room.id}
            onClick={() => onSelect(room.id)}
            className={`w-full text-left p-3 rounded border transition-all duration-200 group
              ${
                isActive
                  ? "border-neon-cyan bg-neon-cyan/10 shadow-neon"
                  : "border-bg-border bg-bg-card/50 hover:border-neon-cyan/50 hover:bg-bg-card"
              }`}
          >
            <div className="flex items-center justify-between gap-2">
              <span
                className={`font-display font-bold text-sm uppercase tracking-wider ${
                  isActive ? "text-neon-cyan" : "text-slate-300"
                }`}
              >
                {room.name}
              </span>
              <div className="flex gap-1">
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
            </div>
            <p className="text-xs text-slate-500 mt-1 line-clamp-2">
              {room.description}
            </p>
            <div className="flex gap-3 mt-2 text-xs text-slate-600">
              <span>{room.items_count} items</span>
              <span>·</span>
              <span>{room.puzzles_count} puzzles</span>
            </div>
          </button>
        );
      })}
    </div>
  );
}
