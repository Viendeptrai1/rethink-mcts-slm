import sys

def max_final_element(N, sequence):
    # Initialize the dp table
    dp = [[0] * N for _ in range(N)]
    move = [[0] * N for _ in range(N)]

    # Base case: single element sequences
    for i in range(N):
        dp[i][i] = sequence[i]

    # Fill the dp table
    for length in range(2, N + 1):  # length of the subsequence
        for i in range(N - length + 1):
            j = i + length - 1
            if length == 2:
                dp[i][j] = sequence[i] + sequence[j]
                move[i][j] = 1  # Choose the first element
            else:
                option1 = sequence[i] + dp[i + 1][j]
                option2 = sequence[j] + dp[i][j - 1]
                if option1 > option2:
                    dp[i][j] = option1
                    move[i][j] = 1  # Choose the first element
                else:
                    dp[i][j] = option2
                    move[i][j] = 2  # Choose the last element

    # Reconstruct the moves
    result = dp[0][N - 1]
    operations = []
    i, j = 0, N - 1
    while i < j:
        if move[i][j] == 1:
            operations.append(i + 1)
            i += 1
        else:
            operations.append(j + 1)
            j -= 1

    # Print the result
    print(result)
    print(len(operations))
    for op in operations:
        print(op)

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
sequence = list(map(int, data[1:]))

# Call the function
max_final_element(N, sequence)