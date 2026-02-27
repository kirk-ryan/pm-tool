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

export type ChatMessage = { role: "user" | "assistant"; content: string };

export type ChatResponse = { response: string; board: BoardData | null };

export async function sendChat(
  board: BoardData,
  message: string,
  history: ChatMessage[]
): Promise<ChatResponse> {
  const res = await fetch("/api/ai/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ board, message, history }),
  });
  if (!res.ok) throw new Error(`POST /api/ai/chat failed: ${res.status}`);
  return res.json() as Promise<ChatResponse>;
}
