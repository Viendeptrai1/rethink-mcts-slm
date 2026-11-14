import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    covered = [False] * 367  # Days are 1 to 365

    for _ in range(n):
        s = int(next(iterator))
        t = int(next(iterator))
        for day in range(s, t + 1):
            covered[day] = True

    count = sum(covered)
    print(count)

if __name__ == "__main__":
    solve()