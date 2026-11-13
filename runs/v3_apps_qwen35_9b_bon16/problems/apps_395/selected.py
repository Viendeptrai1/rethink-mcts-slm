import sys

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        a = list(map(int, line.split()))
        total = sum(a)
        if total % 2 != 0:
            print("NO")
            return
        target = total // 2
        # We need to find if there exists a subset of size 3 that sums to target
        # Since n=6, we can just try all combinations of 3
        from itertools import combinations
        found = False
        for combo in combinations(a, 3):
            if sum(combo) == target:
                found = True
                break
        if found:
            print("YES")
        else:
            print("NO")
    except Exception:
        pass

if __name__ == "__main__":
    solve()