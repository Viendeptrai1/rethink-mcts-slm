import sys
from collections import Counter

def is_palindromic(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[n-1-i][n-1-j]:
                return False
    return True

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    
    if len(numbers) != n * n:
        print("NO")
        return
    
    count = Counter(numbers)
    if any(v % 2 != 0 for v in count.values()):
        print("NO")
        return
    
    matrix = [[0] * n for _ in range(n)]
    
    def fill_matrix(x, y):
        if x == n // 2 and y == n // 2 and n % 2 == 1:
            for num in numbers:
                if count[num] > 0:
                    matrix[x][y] = num
                    count[num] -= 1
                    return True
            return False
        
        if x >= n or y >= n:
            return True
        
        if matrix[x][y] != 0:
            return fill_matrix(x + (y == n - 1), y + 1)
        
        for num in numbers:
            if count[num] > 0:
                matrix[x][y] = num
                matrix[y][x] = num
                matrix[n-1-x][n-1-y] = num
                matrix[n-1-y][n-1-x] = num
                count[num] -= 4
                
                if fill_matrix(x + (y == n - 1), y + 1):
                    return True
                
                matrix[x][y] = 0
                matrix[y][x] = 0
                matrix[n-1-x][n-1-y] = 0
                matrix[n-1-y][n-1-x] = 0
                count[num] += 4
        
        return False
    
    if fill_matrix(0, 0):
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

solve()