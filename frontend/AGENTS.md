# Frontend Code Description

The frontend is a NextJS 16 application with React 19, built as a demo Kanban board.

## Structure

- `src/app/`: NextJS app router. `page.tsx` renders `KanbanBoard`. `layout.tsx` sets up fonts and metadata.

- `src/components/`: React components for the Kanban board.

  - `KanbanBoard.tsx`: Main component, manages board state, handles drag and drop with @dnd-kit, renders columns. Fetches board from API on load; persists changes via API. Renders `ChatWidget`.

  - `KanbanColumn.tsx`: Represents a column, droppable, contains sortable cards, has rename input, card count, NewCardForm.

  - `KanbanCard.tsx`: Individual card, sortable, shows title/details, delete button.

  - `KanbanCardPreview.tsx`: Simplified card for drag overlay.

  - `NewCardForm.tsx`: Form to add new cards, toggles open/closed.

  - `ChatWidget.tsx`: Floating AI chat button (bottom-right FAB) + compact chat panel. Opens on click, closes on backdrop click or close button. Sends messages to `POST /api/ai/chat`; applies board updates when the AI returns one. Maintains conversation history.

- `src/lib/`: Logic.

  - `kanban.ts`: Types (Card, Column, BoardData), initialData with sample data, moveCard function for drag logic, createId.

  - `kanban.test.ts`: Unit tests for moveCard.

  - `api.ts`: `fetchBoard`, `saveBoard`, `sendChat` — all backend API calls.

- Tests: Unit tests with Vitest, e2e with Playwright.

- Styling: TailwindCSS with custom CSS variables for colors.

The app is a working demo with drag and drop, add/edit/delete cards, rename columns.