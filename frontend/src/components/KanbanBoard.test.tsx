import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { AuthProvider } from "@/lib/auth";
import { KanbanBoard } from "@/components/KanbanBoard";

// vi.mock is hoisted before imports, so board data must be defined with vi.hoisted.
const mockBoard = vi.hoisted(() => ({
  columns: [
    { id: "col-backlog",   title: "Backlog",      cardIds: [] },
    { id: "col-discovery", title: "Discovery",    cardIds: [] },
    { id: "col-progress",  title: "In Progress",  cardIds: [] },
    { id: "col-review",    title: "Review",       cardIds: [] },
    { id: "col-done",      title: "Done",         cardIds: [] },
  ],
  cards: {},
}));

vi.mock("@/lib/api", () => ({
  fetchBoard: vi.fn().mockResolvedValue(mockBoard),
  saveBoard: vi.fn().mockResolvedValue(undefined),
}));

const renderBoard = () =>
  render(
    <AuthProvider>
      <KanbanBoard />
    </AuthProvider>
  );

beforeEach(() => {
  sessionStorage.clear();
});

describe("KanbanBoard", () => {
  it("renders five columns", async () => {
    renderBoard();
    expect(await screen.findAllByTestId(/column-/i)).toHaveLength(5);
  });

  it("renames a column", async () => {
    renderBoard();
    const columns = await screen.findAllByTestId(/column-/i);
    const column = columns[0];
    const input = within(column).getByLabelText("Column title");
    await userEvent.clear(input);
    await userEvent.type(input, "New Name");
    expect(input).toHaveValue("New Name");
  });

  it("adds and removes a card", async () => {
    renderBoard();
    const columns = await screen.findAllByTestId(/column-/i);
    const column = columns[0];
    const addButton = within(column).getByRole("button", {
      name: /add a card/i,
    });
    await userEvent.click(addButton);

    const titleInput = within(column).getByPlaceholderText(/card title/i);
    await userEvent.type(titleInput, "New card");
    const detailsInput = within(column).getByPlaceholderText(/details/i);
    await userEvent.type(detailsInput, "Notes");

    await userEvent.click(within(column).getByRole("button", { name: /add card/i }));

    expect(within(column).getByText("New card")).toBeInTheDocument();

    const deleteButton = within(column).getByRole("button", {
      name: /delete new card/i,
    });
    await userEvent.click(deleteButton);

    expect(within(column).queryByText("New card")).not.toBeInTheDocument();
  });

  it("renders a sign out button", async () => {
    renderBoard();
    expect(await screen.findByRole("button", { name: /sign out/i })).toBeInTheDocument();
  });
});
