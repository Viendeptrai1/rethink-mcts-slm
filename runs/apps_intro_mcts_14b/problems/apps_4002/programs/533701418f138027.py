import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    def max_subset_sum_mod_k(row, mod):
        max_sum = 0
        for r in range(min(m // 2 + 1, len(row))):
            for combo in combinations(row, r):
                if sum(combo) % mod == 0:
                    max_sum = max(max_sum, sum(combo))
        return max_sum

    dp = [[0] * (m // 2 + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(m // 2 + 1):
            dp[i][j] = dp[i - 1][j]
            if j > 0:
                dp[i][j] = max(dp[i][j], dp[i - 1][j - 1] + max_subset_sum_mod_k(matrix[i - 1], k))
    
    return dp[n][m // 2]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    k = int(data[index + 2])
    index += 3
    
    matrix = []
    for i in range(n):
        row = list(map(int, data[index:index + m]))
        matrix.append(row)
        index += m
    
    result = max_sum_divisible_by_k(n, m, k, matrix)
    print(result)

if __name__ == "__main__":
    main()