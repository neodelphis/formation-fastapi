import { useCallback, useEffect, useState } from "react";
import { api } from "./api/client";
import type {
  Player,
  Puzzle,
  PuzzleSubmissionResult,
  Room,
  RoomSummary,
} from "./api/types";
import { Header } from "./components/Header";
import { RoomList } from "./components/RoomList";
import { RoomDetail } from "./components/RoomDetail";
import { PlayerPanel } from "./components/PlayerPanel";
import { PuzzleModal } from "./components/PuzzleModal";
import { ResultBanner } from "./components/ResultBanner";
import { Card, SectionTitle } from "./components/Card";

export default function App() {
  const [rooms, setRooms] = useState<RoomSummary[]>([]);
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null);
  const [selectedRoomId, setSelectedRoomId] = useState<string | null>(null);
  const [players, setPlayers] = useState<Player[]>([]);
  const [currentPlayerId, setCurrentPlayerId] = useState<string | null>(null);

  const [puzzleModal, setPuzzleModal] = useState<{
    open: boolean;
    puzzle: Puzzle | null;
  }>({ open: false, puzzle: null });
  const [lastResult, setLastResult] = useState<PuzzleSubmissionResult | null>(
    null
  );
  const [error, setError] = useState<string | null>(null);

  // --- Chargement initial
  const refreshRooms = useCallback(async () => {
    try {
      const list = await api.listRooms();
      setRooms(list);
      if (list.length > 0 && !selectedRoomId) {
        setSelectedRoomId(list[0].id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur API");
    }
  }, [selectedRoomId]);

  const refreshPlayers = useCallback(async () => {
    try {
      const list = await api.listPlayers();
      setPlayers(list);
      if (list.length > 0 && !currentPlayerId) {
        setCurrentPlayerId(list[0].id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur API");
    }
  }, [currentPlayerId]);

  const refreshRoomDetail = useCallback(async () => {
    if (!selectedRoomId) return;
    try {
      const room = await api.getRoom(selectedRoomId);
      setSelectedRoom(room);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur API");
    }
  }, [selectedRoomId]);

  useEffect(() => {
    refreshRooms();
    refreshPlayers();
  }, [refreshRooms, refreshPlayers]);

  useEffect(() => {
    refreshRoomDetail();
  }, [refreshRoomDetail]);

  // --- Handlers
  const handleSelectRoom = (id: string) => {
    setSelectedRoomId(id);
  };

  const handlePickupItem = async (itemId: string) => {
    if (!currentPlayerId) return;
    try {
      await api.pickupItem(currentPlayerId, itemId);
      await refreshPlayers();
      setLastResult({
        success: true,
        message: `Item ramassé : ${itemId}`,
        unlocked_door_id: null,
        reward_item_ids: [],
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur");
    }
  };

  const handleOpenPuzzle = (puzzleId: string) => {
    const puzzle = selectedRoom?.puzzles.find((p) => p.id === puzzleId);
    if (puzzle) {
      setPuzzleModal({ open: true, puzzle });
    }
  };

  const handleSubmitPuzzle = async (code: string) => {
    if (!currentPlayerId || !puzzleModal.puzzle) {
      return { success: false, message: "Aucun joueur ou puzzle sélectionné." };
    }
    try {
      const result = await api.submitPuzzle({
        puzzle_id: puzzleModal.puzzle.id,
        attempt_code: code,
        player_id: currentPlayerId,
      });
      setLastResult(result);
      // Rafraîchit l'état (la porte peut avoir été déverrouillée).
      await Promise.all([refreshRoomDetail(), refreshPlayers()]);
      return result;
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erreur";
      return { success: false, message: msg };
    }
  };

  const currentPlayer = players.find((p) => p.id === currentPlayerId);

  return (
    <div className="min-h-screen relative">
      <div className="scanline" />
      <Header />

      <main className="max-w-7xl mx-auto px-6 py-8 relative z-10">
        {/* Bannière d'erreur globale */}
        {error && (
          <div className="mb-6 p-4 border border-neon-pink/50 bg-neon-pink/10 rounded text-neon-pink text-sm flex items-center justify-between">
            <span>⚠ {error}</span>
            <button onClick={() => setError(null)} className="text-xs">
              ✕
            </button>
          </div>
        )}

        {/* Bannière de brief */}
        <Card glow className="mb-8">
          <div className="flex items-start gap-4">
            <div className="text-4xl">🛰️</div>
            <div>
              <h2 className="font-display font-black text-xl neon-text uppercase mb-2">
                Brief de mission
              </h2>
              <p className="text-sm text-slate-400 leading-relaxed">
                Vous infiltrez le mainframe de Neo-Tokyo contrôlé par l'
                <span className="text-neon-pink">IA Sentinel</span>. Explorez
                les salles, ramassez les items, résolvez les puzzles (codes en
                clair et hashes SHA-256) et déclenchez l'auto-destruction du
                système pour libérer le réseau.
              </p>
            </div>
          </div>
        </Card>

        {/* Layout principal : 3 colonnes */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Colonne gauche : salles + joueur */}
          <div className="lg:col-span-3 space-y-6">
            <Card>
              <SectionTitle title="Salles" icon="▣" />
              <RoomList
                rooms={rooms}
                selectedId={selectedRoomId}
                onSelect={handleSelectRoom}
              />
            </Card>
            <PlayerPanel
              players={players}
              currentPlayerId={currentPlayerId}
              onSelectPlayer={setCurrentPlayerId}
              onRefresh={refreshPlayers}
            />
          </div>

          {/* Colonne droite : détail de la salle */}
          <div className="lg:col-span-9">
            {selectedRoom ? (
              <RoomDetail
                room={selectedRoom}
                onPickupItem={handlePickupItem}
                onSolvePuzzle={handleOpenPuzzle}
                inventory={currentPlayer?.inventory ?? []}
              />
            ) : (
              <Card>
                <p className="text-slate-500 text-center py-12">
                  Chargement des salles...
                </p>
              </Card>
            )}
          </div>
        </div>

        {/* Footer de crédits */}
        <footer className="mt-12 pt-6 border-t border-bg-border text-center text-xs text-slate-600">
          <p>
            DigitalEscape Studio · Operation: Neon Cyberpunk · FastAPI + React
            + Docker
          </p>
          <p className="mt-1">
            Docs API :{" "}
            <a
              href="/api/docs"
              target="_blank"
              rel="noreferrer"
              className="text-neon-cyan hover:underline"
            >
              /api/docs
            </a>{" "}
            ·{" "}
            <a
              href="/api/health"
              target="_blank"
              rel="noreferrer"
              className="text-neon-cyan hover:underline"
            >
              /api/health
            </a>
          </p>
        </footer>
      </main>

      {/* Modale de puzzle */}
      <PuzzleModal
        open={puzzleModal.open}
        puzzleName={puzzleModal.puzzle?.name ?? ""}
        puzzleKind={puzzleModal.puzzle?.puzzle_kind ?? null}
        onClose={() => setPuzzleModal({ open: false, puzzle: null })}
        onSubmit={handleSubmitPuzzle}
      />

      {/* Bannière de résultat */}
      <ResultBanner
        result={lastResult}
        onDismiss={() => setLastResult(null)}
      />
    </div>
  );
}
