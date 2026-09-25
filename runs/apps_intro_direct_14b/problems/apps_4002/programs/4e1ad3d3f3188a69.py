import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    def knapsack(weights, values, W):
        dp = [0] * (W + 1)
        for weight, value in zip(weights, values):
            for w in range(W, weight - 1, -1):
                dp[w] = max(dp[w], dp[w - weight] + value)
        return dp[W]

    max_sum = 0
    for i in range(n):
        row = matrix[i]
        row.sort(reverse=True)
        row = row[:m // 2]
        weights = row
        values = row
        max_sum += knapsack(weights, values, k - 1)

    return max_sum

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
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        matrix.append(row)
        index += m
    
    result = max_sum_divisible_by_k(n, m, k, matrix)
    print(result)

if __name__ == "__main__":
    main()