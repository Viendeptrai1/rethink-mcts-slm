import sys

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        n = int(line)
    except ValueError:
        return

    s = str(n)
    total_digits = len(s)
    total = 0

    # Count full ranges for odd digit lengths less than total_digits
    for d in range(1, total_digits, 2):
        count = 9 * (10 ** (d - 1))
        total += count

    # Count numbers with exactly total_digits that are <= n and have odd length
    if total_digits % 2 == 1:
        total += n - (10 ** (total_digits - 1)) + 1

    print(total)

if __name__ == "__main__":
    solve()