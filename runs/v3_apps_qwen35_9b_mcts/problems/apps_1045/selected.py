import sys

def solve():
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return
        n = int(input_data)
    except ValueError:
        return

    height = 0
    cubes_used = 0
    current_level_cubes = 0

    while True:
        height += 1
        current_level_cubes += height
        if cubes_used + current_level_cubes > n:
            break
        cubes_used += current_level_cubes

    print(height - 1)

if __name__ == "__main__":
    solve()