import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    def knapsack_mod_k(weights, values, W, mod):
        dp = [[0] * (W + 1) for _ in range(mod)]
        for w, v in zip(weights, values):
            for i in range(W, w - 1, -1):
                dp[v % mod][i] = max(dp[v % mod][i], dp[(v - w) % mod][i - w] + w)
        return dp[0][W]

    max_sum = 0
    for row in matrix:
        row.sort(reverse=True)
        weights = row[:m // 2]
        values = weights
        max_sum += knapsack_mod_k(weights, values, sum(weights), k)

    return max_sum

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    matrix = []
    index = 3
    for i in range(n):
        row = list(map(int, data[index:index + m]))
        matrix.append(row)
        index += m
    
    result = max_sum_divisible_by_k(n, m, k, matrix)
    print(result)

if __name__ == "__main__":
    main()