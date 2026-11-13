def count_paths_to_castle():
    import sys
    input = sys.stdin.read
    MOD = 1000003

    data = input().strip().split('\n')
    Y, X, x_init = map(int, data[0].split())
    grid = [list(data[i + 1]) for i in range(Y)]

    # Initialize a DP table where dp[y][x] will store the number of ways to reach the castle from (y, x)
    dp = [[0] * X for _ in range(Y)]

    # Find the position of the castle
    castle_y, castle_x = None, None
    for y in range(Y):
        for x in range(X):
            if grid[y][x] == '@':
                castle_y, castle_x = y, x
                break
        if castle_y is not None:
            break

    # Base case: there's only one way to be at the castle
    dp[castle_y][castle_x] = 1

    # Fill the DP table from the bottom row to the top row
    for y in range(Y - 1, -1, -1):
        for x in range(X):
            if grid[y][x] == '#':
                continue

            # If there's a current, we can only move in the direction of the current
            if grid[y][x] == '>':
                if x + 1 < X and grid[y][x + 1] != '<':
                    dp[y][x] = (dp[y][x] + dp[y][x + 1]) % MOD
            elif grid[y][x] == '<':
                if x - 1 >= 0 and grid[y][x - 1] != '>':
                    dp[y][x] = (dp[y][x] + dp[y][x - 1]) % MOD
            else:
                # If there's no current, we can move north or in the direction of the current
                if y + 1 < Y:
                    dp[y][x] = (dp[y][x] + dp[y + 1][x]) % MOD
                if grid[y][x] == '>':
                    if x + 1 < X and grid[y][x + 1] != '<':
                        dp[y][x] = (dp[y][x] + dp[y][x + 1]) % MOD
                elif grid[y][x] == '<':
                    if x - 1 >= 0 and grid[y][x - 1] != '>':
                        dp[y][x] = (dp[y][x] + dp[y][x - 1]) % MOD

    # The answer is the number of ways to reach the castle from the starting position
    result = dp[0][x_init]
    if result == 0:
        print("begin repairs")
    else:
        print(result)