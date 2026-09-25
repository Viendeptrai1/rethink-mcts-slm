import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    def dp(row, mask):
        if row == n:
            return 0
        if (row, mask) in memo:
            return memo[(row, mask)]
        
        max_sum = 0
        for i in range(m):
            if mask & (1 << i):
                continue
            new_mask = mask | (1 << i)
            current_sum = sum(matrix[row][j] for j in range(m) if new_mask & (1 << j))
            if current_sum % k == 0:
                max_sum = max(max_sum, current_sum + dp(row + 1, new_mask))
            else:
                max_sum = max(max_sum, dp(row + 1, new_mask))
        
        memo[(row, mask)] = max_sum
        return max_sum

    memo = {}
    return dp(0, 0)

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