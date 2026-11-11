import sys

def max_final_element(N, a):
    # Initialize the dp table
    dp = [[0] * N for _ in range(N)]
    move = [[0] * N for _ in range(N)]
    
    # Base case: single element sequences
    for i in range(N):
        dp[i][i] = a[i]
    
    # Fill the dp table
    for length in range(2, N + 1):  # length of the subsequence
        for i in range(N - length + 1):
            j = i + length - 1
            if length == 2:
                dp[i][j] = a[i] + a[j]
                move[i][j] = 1
            else:
                # Option 1: Remove the first element
                option1 = dp[i + 1][j]
                # Option 2: Remove the last element
                option2 = dp[i][j - 1]
                # Option 3: Replace the middle element with the sum of its neighbors
                option3 = a[i] + a[j] + dp[i + 1][j - 1]
                
                dp[i][j] = max(option1, option2, option3)
                if dp[i][j] == option1:
                    move[i][j] = 1
                elif dp[i][j] == option2:
                    move[i][j] = 2
                else:
                    move[i][j] = 3
    
    # Reconstruct the sequence of moves
    i, j = 0, N - 1
    operations = []
    while i < j:
        if move[i][j] == 1:
            operations.append(i + 1)
            i += 1
        elif move[i][j] == 2:
            operations.append(j + 1)
            j -= 1
        else:
            operations.append(i + 1)
            operations.append(j + 1)
            i += 1
            j -= 1
    
    # If there's one element left, add it to the operations
    if i == j:
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