import sys

def solve():
    line = sys.stdin.readline().strip()
    if not line:
        return
    words = line.split()
    seen = set()
    for word in words:
        if word in seen:
            print("no")
            return
        seen.add(word)
    print("yes")

if __name__ == "__main__":
    solve()