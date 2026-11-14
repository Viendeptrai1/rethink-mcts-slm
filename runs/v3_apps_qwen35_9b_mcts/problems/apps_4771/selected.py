import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        V = int(next(iterator))
    except StopIteration:
        return

    max_volume = -1

    for _ in range(n):
        l = int(next(iterator))
        w = int(next(iterator))
        h = int(next(iterator))
        volume = l * w * h
        if volume > max_volume:
            max_volume = volume

    print(max_volume - V)

if __name__ == "__main__":
    solve()