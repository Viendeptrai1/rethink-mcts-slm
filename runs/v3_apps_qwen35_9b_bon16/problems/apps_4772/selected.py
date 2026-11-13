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

    # Check horizontal words
    for r in range(R):
        current_word = []
        for c in range(C):
            if grid[r][c] == '#':
                if len(current_word) >= 2:
                    words.append("".join(current_word))
                current_word = []
            else:
                current_word.append(grid[r][c])
        if len(current_word) >= 2:
            words.append("".join(current_word))

    # Check vertical words
    for c in range(C):
        current_word = []
        for r in range(R):
            if grid[r][c] == '#':
                if len(current_word) >= 2:
                    words.append("".join(current_word))
                current_word = []
            else:
                current_word.append(grid[r][c])
        if len(current_word) >= 2:
            words.append("".join(current_word))

    words.sort()
    print(words[0])

if __name__ == "__main__":
    solve()