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

    days = set()
    for _ in range(n):
        s = int(next(iterator))
        t = int(next(iterator))
        for day in range(s, t + 1):
            days.add(day)

    print(len(days))

if __name__ == "__main__":
    solve()