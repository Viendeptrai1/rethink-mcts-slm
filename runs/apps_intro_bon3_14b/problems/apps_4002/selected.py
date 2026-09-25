import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    def knapsack_modulo(weights, k):
        dp = [0] * k
        for weight in weights:
            new_dp = dp[:]
            for i in range(k):
                new_dp[(i + weight) % k] = max(new_dp[(i + weight) % k], dp[i] + weight)
            dp = new_dp
        return dp[0]

    max_sum = 0
    for row in matrix:
        row.sort(reverse=True)
        max_elements = min(m // 2, len(row))
        best_sum = 0
        for r in range(1, max_elements + 1):
            for combo in combinations(row, r):
                current_sum = sum(combo)
                if current_sum % k == 0:
                    best_sum = max(best_sum, current_sum)
                else:
                    best_sum = max(best_sum, current_sum - (current_sum % k) + k)
        max_sum += best_sum

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