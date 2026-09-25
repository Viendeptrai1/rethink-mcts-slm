import sys
from itertools import combinations

def max_sum_divisible_by_k(n, m, k, matrix):
    def get_max_sum(row):
        max_sum = 0
        for r in range(1, min(m // 2 + 1, len(row)) + 1):
            for combo in combinations(row, r):
                current_sum = sum(combo)
                if current_sum % k == 0:
                    max_sum = max(max_sum, current_sum)
        return max_sum

    total_max_sum = 0
    for row in matrix:
        total_max_sum += get_max_sum(row)

    return total_max_sum

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
    for i in range(n):
        row = list(map(int, data[index:index + m]))
        index += m
        matrix.append(row)
    
    result = max_sum_divisible_by_k(n, m, k, matrix)
    print(result)

if __name__ == "__main__":
    main()