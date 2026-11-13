def count_paths_to_castle():
    import sys
    input = sys.stdin.read
    MOD = 1000003

    data = input().strip().split('\n')
    Y, X, x_init = map(int, data[0].split())
    grid = [list(data[i + 1]) for i in range(Y)]

    # Initialize a DP table with zeros
    dp = [[0] * X for _ in range(Y)]
    dp[Y - 1][x_init] = 1  # Start position

    # Fill the DP table
    for y in range(Y - 1, -1, -1):
        for x in range(X):
            if grid[y][x] == '#':
                continue
            if y < Y - 1:
                dp[y][x] = (dp[y][x] + dp[y + 1][x]) % MOD
            if grid[y][x] == '>':
                if x + 1 < X and grid[y][x + 1] != '<':
                    dp[y][x] = (dp[y][x] + dp[y][x + 1]) % MOD
            elif grid[y][x] == '<':
                if x - 1 >= 0 and grid[y][x - 1] != '>':
                    dp[y][x] = (dp[y][x] + dp[y][x - 1]) % MOD

    # Find the position of the castle
    castle_x, castle_y = None, None
    for y in range(Y):
        for x in range(X):
            if grid[y][x] == '@':
                castle_x, castle_y = x, y
                break
        if castle_x is not None:
            break

    # Output the result
    if castle_x is None or castle_y is None:
        print("begin repairs")
    else:
        print(dp[castle_y][castle_x])