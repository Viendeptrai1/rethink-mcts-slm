import sys

def max_ones(n):
    return n * (n + 1) // 2

def construct_matrix(n, k):
    if k > max_ones(n):
        return -1
    
    result = [[0] * n for _ in range(n)]
    
    i, j = 0, 0
    count = 0
    
    while count < k:
        if i == j:
            result[i][j] = 1
            count += 1
        elif i < j:
            result[i][j] = 1
            result[j][i] = 1
            count += 2
        else:
            break
        
        if count >= k:
            break
        
        if j == n - 1:
            i += 1
            j = i
        else:
            j += 1
    
    return result

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    matrix = construct_matrix(n, k)
    
    if matrix == -1:
        print(-1)
    else:
        print_matrix(matrix)