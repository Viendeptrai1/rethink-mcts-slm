import sys

def max_final_element(N, a):
    # Initialize the dp table
    dp = [[0] * N for _ in range(N)]
    move = [[0] * N for _ in range(N)]

    # Base case: single element subarrays
    for i in range(N):
        dp[i][i] = a[i]

    # Fill the dp table
    for length in range(2, N + 1):  # length of the subarray
        for i in range(N - length + 1):
            j = i + length - 1
            if length == 2:
                dp[i][j] = a[i] + a[j]
                move[i][j] = 1  # Choose the first element
            else:
                if dp[i + 1][j] >= dp[i][j - 1]:
                    dp[i][j] = dp[i + 1][j] + a[i]
                    move[i][j] = 1  # Choose the first element
                else:
                    dp[i][j] = dp[i][j - 1] + a[j]
                    move[i][j] = 2  # Choose the last element

    # Reconstruct the sequence of moves
    i, j = 0, N - 1
    operations = []
    while i < j:
        if move[i][j] == 1:
            operations.append(i + 1)
            i += 1
        else:
            operations.append(j + 1)
            j -= 1

    # Add the last remaining element
    operations.append(i + 1)

    return dp[0][N - 1], len(operations), operations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    max_value, num_operations, operations = max_final_element(N, a)
    
    print(max_value)
    print(num_operations)
    for op in operations:
        print(op)

if __name__ == "__main__":
    main()