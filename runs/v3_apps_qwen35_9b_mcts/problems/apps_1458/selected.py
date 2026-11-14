import sys

def solve():
    try:
        input = sys.stdin.read
        data = input().split()
        if not data:
            return
        n = int(data[0])
        s = list(data[1])
    except Exception:
        return

    for i in range(n - 1):
        if s[i] > s[i + 1]:
            print("YES")
            print(i + 1, i + 2)
            return

    print("NO")

if __name__ == "__main__":
    solve()