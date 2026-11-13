import sys

def solve():
    n = int(sys.stdin.read().strip())
    for d in range(1, 10):
        candidate = int(str(d) * 3)
        if candidate >= n:
            print(candidate)
            return
    for d in range(1, 10):
        candidate = int(str(d) * 4)
        if candidate >= n:
            print(candidate)
            return

if __name__ == "__main__":
    solve()