import sys
from functools import lru_cache

def max_sum_divisible_by_k(n, m, k, matrix):
    @lru_cache(None)
    def dp(row, taken, current_sum):
        if row == n:
            return current_sum if current_sum % k == 0 else -float('inf')
        
        max_sum = dp(row + 1, 0, current_sum)
        for col in range(m):
            if taken < m // 2:
                max_sum = max(max_sum, dp(row, taken + 1, current_sum + matrix[row][col]))
        
        return max_sum
    
    result = dp(0, 0, 0)
    return result if result != -float('inf') else 0

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
    
    result = max_sum_divisible_by_k(n, m, k, tuple(map(tuple, matrix)))
    print(result)

if __name__ == "__main__":
    main()