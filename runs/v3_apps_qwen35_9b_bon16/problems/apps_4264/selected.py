import sys

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        n = int(line)
    except ValueError:
        return

    total = 0
    for x in range(1, n + 1):
        s = str(x)
        if len(s) % 2 == 1:
            total += 1
    print(total)

if __name__ == "__main__":
    solve()