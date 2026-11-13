import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    n = int(line)
    s = str(n)
    d = len(s)
    if d % 2 == 1:
        # All numbers with 1, 3, ..., d-1 digits are fully included
        # Plus numbers with d digits that have odd length (which is all d-digit numbers since d is odd)
        # But we only go up to n, so we include all d-digit numbers from 10^(d-1) to n
        count = 0
        for length in range(1, d, 2):
            count += 9 * (10 ** (length - 1))
        count += (n - 10**(d-1) + 1)
        print(count)
    else:
        # d is even, so we include all numbers with 1, 3, ..., d-1 digits
        # We do NOT include any d-digit numbers because d is even
        count = 0
        for length in range(1, d, 2):
            count += 9 * (10 ** (length - 1))
        print(count)

if __name__ == "__main__":
    solve()