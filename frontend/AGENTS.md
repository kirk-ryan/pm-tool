# Frontend Code Description

The frontend is a NextJS 16 application with React 19, built as a demo Kanban board.

## Structure

- `src/app/`: NextJS app router. `page.tsx` renders `KanbanBoard`. `layout.tsx` sets up fonts and metadata.

- `src/components/`: React components for the Kanban board.

  - `KanbanBoard.tsx`: Main component, manages board state, handles drag and drop with @dnd-kit, renders columns.

  - `KanbanColumn.tsx`: Represents a column, droppable, contains sortable cards, has rename input, card count, NewCardForm.

  - `KanbanCard.tsx`: Individual card, sortable, shows title/details, delete button.

  - `KanbanCardPreview.tsx`: Simplified card for drag overlay.

  - `NewCardForm.tsx`: Form to add new cards, toggles open/closed.

- `src/lib/`: Logic.

  - `kanban.ts`: Types (Card, Column, BoardData), initialData with sample data, moveCard function for drag logic, createId.

  - `kanban.test.ts`: Unit tests for moveCard.

- Tests: Unit tests with Vitest, e2e with Playwright.

- Styling: TailwindCSS with custom CSS variables for colors.

The app is a working demo with drag and drop, add/edit/delete cards, rename columns.