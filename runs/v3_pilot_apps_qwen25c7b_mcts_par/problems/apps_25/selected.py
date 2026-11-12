import sys

def max_symmetric_matrix(n, k):
    if k > n * (n + 1) // 2:
        return -1
    
    result = [[0] * n for _ in range(n)]
    
    ones_needed = k
    for i in range(n):
        for j in range(i, n):
            if ones_needed == 0:
                break
            if i == j:
                result[i][j] = 1
                ones_needed -= 1
            elif ones_needed >= 2:
                result[i][j] = 1
                result[j][i] = 1
                ones_needed -= 2
    
    return result

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    result = max_symmetric_matrix(n, k)
    if result != -1:
        print_matrix(result)
    else:
        print(-1)