// Client API — wrap Fetch autour du backend FastAPI.
//
// En dev (vite), les requêtes sont proxied via /api -> http://localhost:8000
// (voir vite.config.ts). En prod (nginx), les requêtes partent de /api qui
// est reverse-proxied vers le backend par nginx.conf.

import type {
  HealthStatus,
  Player,
  PlayerCreate,
  PuzzleSubmission,
  PuzzleSubmissionResult,
  Room,
  RoomSummary,
} from "./types";

const API_BASE = "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      // réponse non-JSON
    }
    throw new Error(detail);
  }

  if (res.status === 204) {
    return undefined as T;
  }
  return (await res.json()) as T;
}

export const api = {
  // --- Health
  health: () => request<HealthStatus>("/health"),

  // --- Players
  listPlayers: () => request<Player[]>("/players"),
  getPlayer: (id: string) => request<Player>(`/players/${id}`),
  createPlayer: (payload: PlayerCreate) =>
    request<Player>("/players", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updatePlayer: (id: string, payload: Partial<PlayerCreate>) =>
    request<Player>(`/players/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  deletePlayer: (id: string) =>
    request<void>(`/players/${id}`, { method: "DELETE" }),

  // --- Rooms
  listRooms: () => request<RoomSummary[]>("/rooms"),
  getRoom: (id: string) => request<Room>(`/rooms/${id}`),

  // --- Puzzles
  submitPuzzle: (payload: PuzzleSubmission) =>
    request<PuzzleSubmissionResult>("/puzzles/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // --- Exploration actions
  movePlayer: (playerId: string, roomId: string) =>
    request<{ success: boolean; current_room_id: string }>(
      `/players/${playerId}/move/${roomId}`,
      { method: "POST" }
    ),
  pickupItem: (playerId: string, itemId: string) =>
    request<{ success: boolean; inventory: string[] }>(
      `/players/${playerId}/pickup/${itemId}`,
      { method: "POST" }
    ),
};
