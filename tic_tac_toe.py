
import sys


def clear_screen() -> None:
    """Attempt to clear the terminal screen in a cross-platform way."""
    # Keep it simple and robust without relying on external commands
    print("\n" * 100)


def render_board(cells: list[str]) -> str:
    """Return a human-friendly string representation of the board.

    The board is represented by a flat list of 9 strings ("X", "O", or " ").
    Cells are indexed 0..8, but we display positions 1..9 as a guide.
    """
    def cell(i: int) -> str:
        return cells[i] if cells[i] != " " else str(i + 1)

    row_sep = "-" * 11
    rows = [
        f" {cell(0)} | {cell(1)} | {cell(2)} ",
        f" {cell(3)} | {cell(4)} | {cell(5)} ",
        f" {cell(6)} | {cell(7)} | {cell(8)} ",
    ]
    return f"\n{rows[0]}\n{row_sep}\n{rows[1]}\n{row_sep}\n{rows[2]}\n"


def check_winner(cells: list[str]) -> str | None:
    """Return the winning symbol ("X" or "O") if someone has won, else None."""
    winning_triplets = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),            # diagonals
    ]
    for a, b, c in winning_triplets:
        if cells[a] != " " and cells[a] == cells[b] == cells[c]:
            return cells[a]
    return None


def is_draw(cells: list[str]) -> bool:
    """Return True if the board is full and there is no winner."""
    return all(cell != " " for cell in cells) and check_winner(cells) is None


def get_valid_move(cells: list[str], player_symbol: str) -> int:
    """Prompt the current player for a valid move and return the chosen index (0..8)."""
    while True:
        try:
            raw = input(f"Spelare {player_symbol}, välj en ruta (1-9): ").strip()
            if raw.lower() in {"q", "quit", "exit"}:
                print("Avslutar spelet.")
                sys.exit(0)
            choice = int(raw)
        except ValueError:
            print("Ogiltigt val. Ange ett nummer mellan 1 och 9.")
            continue

        if not 1 <= choice <= 9:
            print("Numret måste vara mellan 1 och 9.")
            continue

        idx = choice - 1
        if cells[idx] != " ":
            print("Rutan är redan upptagen. Välj en annan.")
            continue
        return idx


def play_game() -> None:
    """Run a single game of Tic Tac Toe."""
    cells = [" "] * 9
    current = "X"

    while True:
        clear_screen()
        print("Tre-i-rad (Tic Tac Toe)\n")
        print(render_board(cells))

        move = get_valid_move(cells, current)
        cells[move] = current

        winner = check_winner(cells)
        if winner is not None:
            clear_screen()
            print("Tre-i-rad (Tic Tac Toe)\n")
            print(render_board(cells))
            print(f"Grattis! Spelare {winner} vinner!\n")
            break

        if is_draw(cells):
            clear_screen()
            print("Tre-i-rad (Tic Tac Toe)\n")
            print(render_board(cells))
            print("Oavgjort!\n")
            break

        current = "O" if current == "X" else "X"


def ask_play_again() -> bool:
    """Ask the users if they want to play another game."""
    while True:
        answer = input("Spela igen? (j/n): ").strip().lower()
        if answer in {"j", "ja", "y", "yes"}:
            return True
        if answer in {"n", "nej", "no"}:
            return False
        print("Svara med 'j' eller 'n'.")


def main() -> None:
    print("Välkommen till Tre-i-rad (Tic Tac Toe)!")
    print("Två spelare turas om att välja rutor 1-9. Skriv 'q' för att avsluta.\n")
    while True:
        play_game()
        if not ask_play_again():
            print("Tack för att du spelade! Hej då!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAvslutar. Hej då!")

