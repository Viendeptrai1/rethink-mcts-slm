import sys

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        n = int(line)
    except ValueError:
        return

    x = n
    while True:
        s = str(x)
        if len(set(s)) == 1:
            print(x)
            return
        x += 1

if __name__ == "__main__":
    solve()