import sys

def is_palindromic(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[n-1-i][j] or matrix[i][j] != matrix[i][n-1-j]:
                return False
    return True

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    
    if n == 1:
        print("YES")
        print(numbers[0])
        return
    
    if len(numbers) != n * n:
        print("NO")
        return
    
    # Try to construct a palindromic matrix
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i <= n // 2 and j <= n // 2:
                row.append(numbers.pop(0))
            elif i <= n // 2 and j > n // 2:
                row.append(matrix[i][n - 1 - j])
            elif i > n // 2 and j <= n // 2:
                row.append(matrix[n - 1 - i][j])
            else:
                row.append(matrix[n - 1 - i][n - 1 - j])
        matrix.append(row)
    
    if is_palindromic(matrix):
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

solve()