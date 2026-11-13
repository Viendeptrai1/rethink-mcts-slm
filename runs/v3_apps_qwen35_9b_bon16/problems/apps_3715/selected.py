import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1 + i]))

    # dp[0] -> minimum rest days if last day was rest
    # dp[1] -> minimum rest days if last day was sport
    # dp[2] -> minimum rest days if last day was contest
    dp = [0] * 3

    # Base case: day 1
    if a[0] == 0:
        # Nothing available, must rest
        dp = [1, float('inf'), float('inf')]
    elif a[0] == 1:
        # Only contest available
        dp = [1, float('inf'), 0]
    elif a[0] == 2:
        # Only sport available
        dp = [1, 0, float('inf')]
    elif a[0] == 3:
        # Both available, choose one to minimize rest (rest=0 either way)
        dp = [1, 0, 0]

    for i in range(1, n):
        new_dp = [0] * 3
        val = a[i]

        # Option to rest today
        # We come from any previous state, take the minimum
        new_dp[0] = min(dp) + 1

        # Option to do sport today
        can_sport = (val == 2) or (val == 3)
        if can_sport:
            # Can't come from sport yesterday
            prev_rest = dp[0]
            prev_contest = dp[2]
            new_dp[1] = min(prev_rest, prev_contest)
        else:
            new_dp[1] = float('inf')

        # Option to do contest today
        can_contest = (val == 1) or (val == 3)
        if can_contest:
            # Can't come from contest yesterday
            prev_rest = dp[0]
            prev_sport = dp[1]
            new_dp[2] = min(prev_rest, prev_sport)
        else:
            new_dp[2] = float('inf')

        dp = new_dp

    print(min(dp))

if __name__ == "__main__":
    solve()