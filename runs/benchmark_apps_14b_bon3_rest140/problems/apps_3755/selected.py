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
            # Option 1: Remove the first element
            option1 = dp[i + 1][j]
            # Option 2: Remove the last element
            option2 = dp[i][j - 1]
            # Option 3: Replace the middle element with the sum of its neighbors
            option3 = -float('inf')
            for k in range(i + 1, j):
                if dp[i][k - 1] + dp[k + 1][j] > option3:
                    option3 = dp[i][k - 1] + dp[k + 1][j]
                    move[i][j] = k

            dp[i][j] = max(option1, option2, option3)

    # Reconstruct the sequence of moves
    i, j = 0, N - 1
    result = []
    while i < j:
        if dp[i + 1][j] == dp[i][j]:
            result.append(1)
            i += 1
        elif dp[i][j - 1] == dp[i][j]:
            result.append(j - i + 1)
            j -= 1
        else:
            k = move[i][j]
            result.append(k - i + 1)
            i, j = i, k - 1

    return dp[0][N - 1], len(result), result

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