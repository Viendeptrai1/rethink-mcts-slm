import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]

    # dp[i][0] = min rest days up to day i, ending with rest on day i
    # dp[i][1] = min rest days up to day i, ending with sport on day i
    # dp[i][2] = min rest days up to day i, ending with contest on day i

    # Initialize for day 0 (index 0)
    # If we rest on day 0: 1 rest day
    # If we do sport on day 0: only if gym is open (a[0] == 2 or a[0] == 3)
    # If we do contest on day 0: only if contest is held (a[0] == 1 or a[0] == 3)

    dp = [[float('inf')] * 3 for _ in range(n)]

    # Day 0
    dp[0][0] = 1  # Rest
    if a[0] == 2 or a[0] == 3:
        dp[0][1] = 0  # Sport
    if a[0] == 1 or a[0] == 3:
        dp[0][2] = 0  # Contest

    for i in range(1, n):
        # Option 0: Rest on day i
        dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1

        # Option 1: Sport on day i
        # Allowed if gym is open (a[i] == 2 or a[i] == 3)
        # Previous day must be rest or contest (cannot be sport)
        if a[i] == 2 or a[i] == 3:
            dp[i][1] = min(dp[i-1][0], dp[i-1][2])

        # Option 2: Contest on day i
        # Allowed if contest is held (a[i] == 1 or a[i] == 3)
        # Previous day must be rest or sport (cannot be contest)
        if a[i] == 1 or a[i] == 3:
            dp[i][2] = min(dp[i-1][0], dp[i-1][1])

    print(min(dp[n-1][0], dp[n-1][1], dp[n-1][2]))

if __name__ == "__main__":
    solve()