import { useState } from "react";
import type { Player, PlayerCreate } from "../api/types";
import { api } from "../api/client";
import { Card, SectionTitle } from "./Card";

interface PlayerPanelProps {
  players: Player[];
  currentPlayerId: string | null;
  onSelectPlayer: (id: string) => void;
  onRefresh: () => void;
}

export function PlayerPanel({
  players,
  currentPlayerId,
  onSelectPlayer,
  onRefresh,
}: PlayerPanelProps) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<PlayerCreate>({
    id: "",
    name: "",
    description: "",
  });
  const [error, setError] = useState<string | null>(null);

  const currentPlayer = players.find((p) => p.id === currentPlayerId);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await api.createPlayer(form);
      setForm({ id: "", name: "", description: "" });
      setShowForm(false);
      onRefresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur");
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm(`Supprimer le joueur ${id} ?`)) return;
    try {
      await api.deletePlayer(id);
      onRefresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur");
    }
  };

  return (
    <Card>
      <SectionTitle
        title="Joueurs connectés"
        subtitle="Un escape game se joue à plusieurs"
        icon="◈"
      />

      {/* Liste des joueurs */}
      <div className="space-y-2 mb-4">
        {players.length === 0 && (
          <p className="text-xs text-slate-600 italic">Aucun joueur.</p>
        )}
        {players.map((p) => {
          const isSelected = p.id === currentPlayerId;
          return (
            <div
              key={p.id}
              className={`p-2 rounded border transition-all ${
                isSelected
                  ? "border-neon-cyan bg-neon-cyan/10"
                  : "border-bg-border bg-bg-dark/40"
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <button
                  onClick={() => onSelectPlayer(p.id)}
                  className="flex-1 text-left"
                >
                  <div className="flex items-center gap-2">
                    <span
                      className={`font-bold text-sm ${
                        isSelected ? "text-neon-cyan" : "text-slate-200"
                      }`}
                    >
                      {p.name}
                    </span>
                    <code className="text-xs text-slate-600">#{p.id}</code>
                  </div>
                  {p.description && (
                    <p className="text-xs text-slate-500 mt-0.5 line-clamp-1">
                      {p.description}
                    </p>
                  )}
                </button>
                <button
                  onClick={() => handleDelete(p.id)}
                  className="text-xs text-slate-600 hover:text-neon-pink"
                  aria-label="Supprimer"
                >
                  ✕
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Formulaire de création */}
      {!showForm ? (
        <button
          onClick={() => setShowForm(true)}
          className="btn-cyber w-full text-xs"
        >
          + Nouveau joueur
        </button>
      ) : (
        <form onSubmit={handleCreate} className="space-y-2">
          <input
            placeholder="id (ex: player-2)"
            value={form.id}
            onChange={(e) => setForm({ ...form, id: e.target.value })}
            className="input-cyber text-xs"
            required
            pattern="[a-zA-Z0-9_-]+"
            minLength={3}
          />
          <input
            placeholder="Pseudonyme"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="input-cyber text-xs"
            required
          />
          <input
            placeholder="Description (optionnelle)"
            value={form.description}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
            className="input-cyber text-xs"
          />
          {error && (
            <p className="text-xs text-neon-pink">⚠ {error}</p>
          )}
          <div className="flex gap-2">
            <button type="submit" className="btn-cyber flex-1 text-xs">
              Créer
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="text-xs px-3 py-2 text-slate-500 hover:text-slate-300"
            >
              Annuler
            </button>
          </div>
        </form>
      )}

      {/* Détails du joueur sélectionné */}
      {currentPlayer && (
        <div className="mt-4 pt-4 border-t border-bg-border">
          <h4 className="text-xs uppercase text-slate-500 tracking-wider mb-2">
            État du joueur
          </h4>
          <dl className="space-y-1 text-xs">
            <div className="flex justify-between">
              <dt className="text-slate-500">Salle courante</dt>
              <dd className="text-neon-cyan font-mono">
                {currentPlayer.current_room_id ?? "—"}
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Inventaire</dt>
              <dd className="text-neon-green font-mono">
                {currentPlayer.inventory.length} item(s)
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Puzzles résolus</dt>
              <dd className="text-neon-pink font-mono">
                {currentPlayer.solved_puzzles.length}
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Salles visitées</dt>
              <dd className="text-slate-300 font-mono">
                {currentPlayer.visited_rooms.length}
              </dd>
            </div>
          </dl>
          {currentPlayer.inventory.length > 0 && (
            <div className="mt-2">
              <p className="text-xs text-slate-500 mb-1">Items :</p>
              <div className="flex flex-wrap gap-1">
                {currentPlayer.inventory.map((id) => (
                  <code
                    key={id}
                    className="text-xs px-1.5 py-0.5 bg-bg-dark border border-bg-border rounded text-neon-green"
                  >
                    {id}
                  </code>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </Card>
  );
}
