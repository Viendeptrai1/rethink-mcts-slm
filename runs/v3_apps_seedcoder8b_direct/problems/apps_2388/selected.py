def count_remaining_robot_sets():
    import sys
    input = sys.stdin.read
    MOD = 998244353

    data = input().split()
    N = int(data[0])
    robots = []

    index = 1
    for _ in range(N):
        X_i = int(data[index])
        D_i = int(data[index + 1])
        robots.append((X_i, D_i))
        index += 2

    # Sort robots by their starting position
    robots.sort()

    # dp[mask] will store the number of ways to achieve the state represented by mask
    dp = [0] * (1 << N)
    dp[0] = 1  # Base case: no robots on the line

    for mask in range(1 << N):
        active_robots = [i for i in range(N) if mask & (1 << i)]
        if not active_robots:
            continue

        # Check if we can activate any robot in the current state
        for i in active_robots:
            X_i, D_i = robots[i]
            # Check if this robot can be activated
            can_activate = True
            for j in active_robots:
                if i != j:
                    X_j, D_j = robots[j]
                    if X_j >= X_i and X_j < X_i + D_i:
                        can_activate = False
                        break
            if can_activate:
                # If it can be activated, calculate the new state
                new_mask = mask
                for j in active_robots:
                    X_j, D_j = robots[j]
                    if X_j >= X_i and X_j < X_i + D_i:
                        new_mask &= ~(1 << j)
                dp[new_mask] = (dp[new_mask] + dp[mask]) % MOD

    # Sum up all possible states
    result = sum(dp) % MOD
    print(result)