import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    def knapsack_modulo(weights, values, W, mod):
        dp = [0] * (W + 1)
        for weight, value in zip(weights, values):
            for w in range(W, weight - 1, -1):
                dp[w] = max(dp[w], dp[w - weight] + value)
        return max(dp[i] for i in range(0, W + 1, mod))

    max_sum = 0
    for row in matrix:
        row.sort(reverse=True)
        half_m = m // 2
        for r in range(half_m + 1):
            for combo in combinations(row[:half_m], r):
                current_sum = sum(combo)
                if current_sum % k == 0:
                    max_sum = max(max_sum, current_sum)
                else:
                    max_sum = max(max_sum, current_sum + (k - current_sum % k))
    
    return max_sum

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    m = int(data[index])
    index += 1
    k = int(data[index])
    index += 1
    
    matrix = []
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        index += m
        matrix.append(row)
    
    result = max_sum_divisible_by_k(n, m, k, matrix)
    print(result)

if __name__ == "__main__":
    main()