import sys

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        m, n, t = map(int, line.split())
        
        operations = 0
        if t == 1:
            operations = 1
        elif t == 2:
            operations = 1 << n
        elif t == 3:
            operations = n ** 4
        elif t == 4:
            operations = n ** 3
        elif t == 5:
            operations = n ** 2
        elif t == 6:
            operations = n * (n.bit_length())
        elif t == 7:
            operations = n
        
        if operations <= m:
            print("AC")
        else:
            print("TLE")
    except Exception:
        pass

if __name__ == "__main__":
    solve()