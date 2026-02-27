import type { BoardData } from "./kanban";

export async function fetchBoard(): Promise<BoardData> {
  const res = await fetch("/api/board");
  if (!res.ok) throw new Error(`GET /api/board failed: ${res.status}`);
  return res.json() as Promise<BoardData>;
}

export async function saveBoard(data: BoardData): Promise<void> {
  const res = await fetch("/api/board", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`PUT /api/board failed: ${res.status}`);
}
