
import sys


# ---------- UI Theming (ANSI) ----------
def supports_color() -> bool:
    """Best-effort detection whether ANSI colors are supported."""
    if not sys.stdout.isatty():
        return False
    # Windows 10+ terminals generally support ANSI escape codes
    return True


COLOR_ENABLED = supports_color()


def c(code: str) -> str:
    return code if COLOR_ENABLED else ""


RESET = c("\033[0m")
BOLD = c("\033[1m")
DIM = c("\033[2m")

FG_CYAN = c("\033[36m")
FG_GREEN = c("\033[32m")
FG_MAGENTA = c("\033[35m")
FG_YELLOW = c("\033[33m")
FG_WHITE = c("\033[37m")

BG_YELLOW = c("\033[43m")


def clear_screen() -> None:
    """Clear terminal screen and move cursor to home."""
    if COLOR_ENABLED:
        # ANSI clear and home
        print("\033[2J\033[H", end="")
    else:
        print("\n" * 100)


def render_board(cells: list[str], last_move: int | None = None) -> str:
    """Return a colorful, box-drawn representation of the board.

    The board is represented by a flat list of 9 strings ("X", "O", or " ").
    Cells are indexed 0..8, but we display positions 1..9 as a guide.
    """
    def symbol(i: int) -> str:
        value = cells[i]
        if value == "X":
            return f"{BOLD}{FG_GREEN}X{RESET}"
        if value == "O":
            return f"{BOLD}{FG_MAGENTA}O{RESET}"
        return f"{DIM}{FG_WHITE}{i + 1}{RESET}" if COLOR_ENABLED else str(i + 1)

    def decorate(content: str, i: int) -> str:
        if last_move is not None and i == last_move:
            # Highlight background for the most recent move
            return f"{BG_YELLOW}{content}{RESET}"
        return content

    # Build three rows; each cell is 1 char wide symbol centered in 3 spaces
    top = f"{FG_CYAN}┌───┬───┬───┐{RESET}"
    mid = f"{FG_CYAN}├───┼───┼───┤{RESET}"
    bottom = f"{FG_CYAN}└───┴───┴───┘{RESET}"

    r0 = (
        f"{FG_CYAN}│{RESET} "
        + decorate(symbol(0), 0)
        + f" {FG_CYAN}│{RESET} "
        + decorate(symbol(1), 1)
        + f" {FG_CYAN}│{RESET} "
        + decorate(symbol(2), 2)
        + f" {FG_CYAN}│{RESET}"
    )
    r1 = (
        f"{FG_CYAN}│{RESET} "
        + decorate(symbol(3), 3)
        + f" {FG_CYAN}│{RESET} "
        + decorate(symbol(4), 4)
        + f" {FG_CYAN}│{RESET} "
        + decorate(symbol(5), 5)
        + f" {FG_CYAN}│{RESET}"
    )
    r2 = (
        f"{FG_CYAN}│{RESET} "
        + decorate(symbol(6), 6)
        + f" {FG_CYAN}│{RESET} "
        + decorate(symbol(7), 7)
        + f" {FG_CYAN}│{RESET} "
        + decorate(symbol(8), 8)
        + f" {FG_CYAN}│{RESET}"
    )

    return (
        "\n"
        + top
        + "\n"
        + r0
        + "\n"
        + mid
        + "\n"
        + r1
        + "\n"
        + mid
        + "\n"
        + r2
        + "\n"
        + bottom
        + "\n"
    )


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
    last_move: int | None = None

    while True:
        clear_screen()
        title = f"{BOLD}{FG_CYAN}Tre-i-rad (Tic Tac Toe){RESET}"
        legend_x = f"{BOLD}{FG_GREEN}X{RESET}"
        legend_o = f"{BOLD}{FG_MAGENTA}O{RESET}"
        print(title)
        print(f"{DIM}Välj en ruta 1-9. Skriv 'q' för att avsluta.{RESET}\n")
        print(render_board(cells, last_move))
        turn_color = FG_GREEN if current == "X" else FG_MAGENTA
        print(f"{BOLD}{turn_color}Spelare {current}{RESET} är vid drag.\n")

        move = get_valid_move(cells, current)
        cells[move] = current
        last_move = move

        winner = check_winner(cells)
        if winner is not None:
            clear_screen()
            print(title)
            print()
            print(render_board(cells, last_move))
            wcol = FG_GREEN if winner == "X" else FG_MAGENTA
            print(f"{BOLD}{wcol}Grattis! Spelare {winner} vinner!{RESET}\n")
            break

        if is_draw(cells):
            clear_screen()
            print(title)
            print()
            print(render_board(cells, last_move))
            print(f"{BOLD}{FG_YELLOW}Oavgjort!{RESET}\n")
            break

        current = "O" if current == "X" else "X"


def ask_play_again() -> bool:
    """Ask the users if they want to play another game."""
    while True:
        answer = input(f"{DIM}Spela igen? (j/n): {RESET}").strip().lower()
        if answer in {"j", "ja", "y", "yes"}:
            return True
        if answer in {"n", "nej", "no"}:
            return False
        print(f"{DIM}Svara med 'j' eller 'n'.{RESET}")


def main() -> None:
    print(f"{BOLD}Välkommen till Tre-i-rad (Tic Tac Toe)!{RESET}")
    print(f"{DIM}Två spelare turas om att välja rutor 1-9. Skriv 'q' för att avsluta.{RESET}\n")
    while True:
        play_game()
        if not ask_play_again():
            print(f"{DIM}Tack för att du spelade! Hej då!{RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAvslutar. Hej då!")

