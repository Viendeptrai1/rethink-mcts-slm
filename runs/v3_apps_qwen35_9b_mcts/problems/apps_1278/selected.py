import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    x = int(next(iterator))
    y = int(next(iterator))

    a = []
    for _ in range(n):
        a.append(int(next(iterator)))

    # We need to find the earliest index i (0-based) such that:
    # a[i] < a[j] for all j in [max(0, i-x), i-1]
    # and a[i] < a[j] for all j in [i+1, min(n-1, i+y)]

    # Since n is up to 100,000 and x, y are very small (<= 7),
    # a simple O(n * (x+y)) approach is perfectly efficient.
    # Total operations roughly 100,000 * 14 = 1.4 million, which is well within time limits.

    for i in range(n):
        is_not_so_rainy = True

        # Check x days before
        start_before = max(0, i - x)
        for j in range(start_before, i):
            if a[j] <= a[i]:
                is_not_so_rainy = False
                break
        if not is_not_so_rainy:
            continue

        # Check y days after
        end_after = min(n - 1, i + y)
        for j in range(i + 1, end_after + 1):
            if a[j] <= a[i]:
                is_not_so_rainy = False
                break
        if not is_not_so_rainy:
            continue

        # If we are here, day i satisfies the condition
        print(i + 1)
        return

if __name__ == "__main__":
    solve()