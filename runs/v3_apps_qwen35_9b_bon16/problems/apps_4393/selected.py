import sys

def solve():
    n = int(sys.stdin.readline())
    t = sys.stdin.readline().strip()
    
    s = []
    idx = 0
    for i in range(1, n + 1):
        if idx >= n:
            break
        s.append(t[idx])
        idx += i
    
    print("".join(s))

if __name__ == "__main__":
    solve()