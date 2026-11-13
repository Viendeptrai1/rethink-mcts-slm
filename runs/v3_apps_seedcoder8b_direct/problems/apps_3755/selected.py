def maximize_final_element():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    sequence = list(map(int, data[1:]))
    
    # Dynamic programming table to store the maximum value we can achieve
    # ending at each position with a certain number of operations.
    dp = [[-float('inf')] * (N + 1) for _ in range(N)]
    
    # Base case: with 0 operations, the maximum value is the element itself.
    for i in range(N):
        dp[i][0] = sequence[i]
    
    # Fill the dp table
    for ops in range(1, N):
        for i in range(N - ops):
            j = i + ops
            # If we remove the element at the start
            if i + 1 <= j:
                dp[i][ops] = max(dp[i][ops], dp[i + 1][ops - 1])
            # If we remove the element at the end
            if i <= j - 1:
                dp[i][ops] = max(dp[i][ops], dp[i][ops - 1])
            # If we replace the element in the middle
            if i + 1 < j - 1:
                dp[i][ops] = max(dp[i][ops], dp[i + 2][ops - 1] + sequence[i + 1])
    
    # Find the maximum value we can achieve with N-1 operations
    max_value = max(dp[i][N - 1] for i in range(N))
    
    # Backtrack to find the sequence of operations
    operations = []
    ops = N - 1
    for i in range(N):
        if ops == 0:
            break
        if i + 1 < N and dp[i][ops] == dp[i + 1][ops - 1]:
            operations.append(i + 1)
            ops -= 1
        elif i < N - 1 and dp[i][ops] == dp[i][ops - 1]:
            operations.append(i + 1)
            ops -= 1
        elif i + 2 < N and dp[i][ops] == dp[i + 2][ops - 1] + sequence[i + 1]:
            operations.append(i + 1)
            ops -= 1
    
    # Output the results
    print(max_value)
    print(len(operations))
    for op in operations:
        print(op)