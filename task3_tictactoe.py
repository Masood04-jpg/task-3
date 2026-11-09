"""
Task 3: AI Tic-Tac-Toe using Minimax (with alpha-beta pruning). CLI UI + win/loss tracking.
You are 'X', the AI is 'O'. The AI is unbeatable - the best you can do is draw.
Run: python task3_tictactoe.py
"""
import math

HUMAN, AI, EMPTY = "X", "O", " "
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != EMPTY and b[a] == b[c] == b[d]:
            return b[a]
    return None


def moves(b): return [i for i, v in enumerate(b) if v == EMPTY]
def full(b): return EMPTY not in b


def minimax(b, is_ai, alpha=-math.inf, beta=math.inf, depth=0):
    w = winner(b)
    if w == AI: return 10 - depth      # prefer faster wins
    if w == HUMAN: return depth - 10   # prefer slower losses
    if full(b): return 0
    if is_ai:
        best = -math.inf
        for m in moves(b):
            b[m] = AI
            best = max(best, minimax(b, False, alpha, beta, depth + 1))
            b[m] = EMPTY
            alpha = max(alpha, best)
            if beta <= alpha: break
        return best
    best = math.inf
    for m in moves(b):
        b[m] = HUMAN
        best = min(best, minimax(b, True, alpha, beta, depth + 1))
        b[m] = EMPTY
        beta = min(beta, best)
        if beta <= alpha: break
    return best


def best_move(b):
    best_score, move = -math.inf, None
    for m in moves(b):
        b[m] = AI
        score = minimax(b, False, depth=1)
        b[m] = EMPTY
        if score > best_score:
            best_score, move = score, m
    return move


def show(b):
    print()
    for r in range(3):
        print(" " + " | ".join(b[r * 3:r * 3 + 3]))
        if r < 2: print("---+---+---")
    print()


def play_round(human_first):
    b = [EMPTY] * 9
    turn_human = human_first
    print("\nPositions:\n 1 | 2 | 3\n---+---+---\n 4 | 5 | 6\n---+---+---\n 7 | 8 | 9")
    while True:
        show(b)
        if turn_human:
            while True:
                s = input("Your move (1-9): ").strip()
                if s.isdigit() and 1 <= int(s) <= 9 and b[int(s) - 1] == EMPTY:
                    b[int(s) - 1] = HUMAN
                    break
                print("Invalid move, try again.")
        else:
            m = best_move(b)
            b[m] = AI
            print(f"AI plays {m + 1}")
        w = winner(b)
        if w or full(b):
            show(b)
            return w
        turn_human = not turn_human


def main():
    score = {"wins": 0, "losses": 0, "draws": 0}
    human_first = True
    print("=== Tic-Tac-Toe vs Minimax AI === (you = X, AI = O)")
    while True:
        w = play_round(human_first)
        if w == HUMAN: score["wins"] += 1; print("You win!")
        elif w == AI: score["losses"] += 1; print("AI wins!")
        else: score["draws"] += 1; print("It's a draw!")
        print(f"Score -> Wins: {score['wins']} | Losses: {score['losses']} | Draws: {score['draws']}")
        if input("Play again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break
        human_first = not human_first  # alternate who starts


if __name__ == "__main__":
    main()
