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
    # a[i] < a[j] for all j in [i+1, min(n-1, i+y)]
    #
    # Since x and y are very small (<= 7), we can simply check the neighbors directly.
    # This gives O(n * (x+y)) which is O(n) effectively since x+y is constant and small.

    for i in range(n):
        is_valid = True
        
        # Check x days before
        start_before = max(0, i - x)
        for j in range(start_before, i):
            if a[j] <= a[i]:
                is_valid = False
                break
        if not is_valid:
            continue

        # Check y days after
        end_after = min(n - 1, i + y)
        for j in range(i + 1, end_after + 1):
            if a[j] <= a[i]:
                is_valid = False
                break
        if not is_valid:
            continue

        # Found the earliest day
        print(i + 1)
        return

if __name__ == "__main__":
    solve()