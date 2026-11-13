import sys

def max_elements_in_extremely_cool_submatrix(R, S, matrix):
    dp = [[[0, 0] for _ in range(S)] for _ in range(R)]
    max_size = 0
    
    for i in range(1, R):
        for j in range(1, S):
            for r in range(i):
                for s in range(j):
                    if matrix[i][j] + matrix[r][s] <= matrix[i][s] + matrix[r][j]:
                        dp[i][j][0] = max(dp[i][j][0], dp[r][s][0] + (i - r + 1) * (j - s + 1))
                        dp[i][j][1] = max(dp[i][j][1], dp[r][s][1] + (i - r + 1) * (j - s + 1))
                        max_size = max(max_size, dp[i][j][0], dp[i][j][1])
    
    return max_size

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    S = int(data[1])
    matrix = []
    index = 2
    for i in range(R):
        row = list(map(int, data[index:index+S]))
        matrix.append(row)
        index += S
    
    result = max_elements_in_extremely_cool_submatrix(R, S, matrix)
    print(result)