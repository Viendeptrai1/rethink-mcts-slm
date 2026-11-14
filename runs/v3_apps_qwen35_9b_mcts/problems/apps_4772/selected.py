import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        R = int(next(iterator))
        C = int(next(iterator))
    except StopIteration:
        return

    grid = []
    for _ in range(R):
        grid.append(next(iterator))

    words = []

    # Scan horizontal words
    for r in range(R):
        current_word = []
        for c in range(C):
            char = grid[r][c]
            if char != '#':
                current_word.append(char)
            else:
                if len(current_word) >= 2:
                    words.append("".join(current_word))
                current_word = []
        if len(current_word) >= 2:
            words.append("".join(current_word))

    # Scan vertical words
    for c in range(C):
        current_word = []
        for r in range(R):
            char = grid[r][c]
            if char != '#':
                current_word.append(char)
            else:
                if len(current_word) >= 2:
                    words.append("".join(current_word))
                current_word = []
        if len(current_word) >= 2:
            words.append("".join(current_word))

    if words:
        print(min(words))

if __name__ == "__main__":
    solve()