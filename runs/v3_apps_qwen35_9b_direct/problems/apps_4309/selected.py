import sys

def solve():
    n = int(sys.stdin.read().strip())
    for length in range(1, 4):
        for digit in range(1, 10):
            candidate = int(str(digit) * length)
            if candidate >= n:
                print(candidate)
                return

if __name__ == "__main__":
    solve()