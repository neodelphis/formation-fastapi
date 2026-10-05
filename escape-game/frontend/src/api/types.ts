// Types TypeScript miroir des schémas Pydantic du backend.

export interface HealthStatus {
  status: string;
  game_title: string;
  game_master: string;
  engine_version: string;
}

export interface Player {
  id: string;
  name: string;
  description: string;
  type: string;
  inventory: string[];
  visited_rooms: string[];
  solved_puzzles: string[];
  current_room_id: string | null;
}

export interface PlayerCreate {
  id: string;
  name: string;
  description?: string;
}

export interface Item {
  id: string;
  name: string;
  description: string;
  type: string;
  usable: boolean;
}

export interface Door {
  id: string;
  name: string;
  description: string;
  type: string;
  is_locked: boolean;
  required_item_id: string | null;
  target_room_id: string | null;
}

export interface Puzzle {
  id: string;
  name: string;
  description: string;
  type: string;
  reward_message: string;
  puzzle_kind: string | null;
  hash_algorithm: string | null;
  solution_exposed: boolean;
}

export interface Room {
  id: string;
  name: string;
  description: string;
  type: string;
  items: Item[];
  doors: Door[];
  puzzles: Puzzle[];
  is_start: boolean;
  is_exit: boolean;
}

export interface RoomSummary {
  id: string;
  name: string;
  description: string;
  is_start: boolean;
  is_exit: boolean;
  items_count: number;
  puzzles_count: number;
}

export interface PuzzleSubmission {
  puzzle_id: string;
  attempt_code: string;
  player_id: string;
}

export interface PuzzleSubmissionResult {
  success: boolean;
  message: string;
  unlocked_door_id: string | null;
  reward_item_ids: string[];
}
