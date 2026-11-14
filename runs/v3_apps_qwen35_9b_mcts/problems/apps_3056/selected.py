import sys

def solve():
    s = sys.stdin.read().strip()
    if not s:
        print(0)
        return

    # dp_count: number of paths reaching current level
    # dp_sum: sum of node labels at current level
    dp_count = 1
    dp_sum = 1

    for char in s:
        new_count = 0
        new_sum = 0

        if char == 'L':
            # From each node X, go to 2X
            new_count = dp_count
            new_sum = 2 * dp_sum
        elif char == 'R':
            # From each node X, go to 2X+1
            new_count = dp_count
            new_sum = 2 * dp_sum + dp_count
        elif char == 'P':
            # Stay at X
            new_count = dp_count
            new_sum = dp_sum
        elif char == '*':
            # Three possibilities: L, R, P
            # L: count = dp_count, sum = 2*dp_sum
            # R: count = dp_count, sum = 2*dp_sum + dp_count
            # P: count = dp_count, sum = dp_sum
            new_count = 3 * dp_count
            new_sum = (2 * dp_sum) + (2 * dp_sum + dp_count) + dp_sum
            # Simplify: new_sum = 5*dp_sum + dp_count

        dp_count = new_count
        dp_sum = new_sum

    print(dp_sum)

if __name__ == "__main__":
    solve()