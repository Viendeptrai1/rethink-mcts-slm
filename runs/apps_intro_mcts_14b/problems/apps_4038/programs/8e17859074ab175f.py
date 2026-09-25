import sys

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
    
    if n == 1:
        print("YES")
        print(numbers[0])
        return
    
    # Check if we can form a palindromic matrix
    if len(set(numbers)) != len(numbers):
        print("NO")
        return
    
    # Sort the numbers
    numbers.sort()
    
    # Try to construct the matrix
    matrix = [[0] * n for _ in range(n)]
    index = 0
    
    # Fill the top-left to bottom-right diagonal
    for i in range(n):
        matrix[i][i] = numbers[index]
        index += 1
    
    # Fill the bottom-left to top-right diagonal
    for i in range(n):
        matrix[n-1-i][i] = numbers[index]
        index += 1
    
    # Fill the remaining cells
    for i in range(n):
        for j in range(i+1, n-i-1):
            matrix[i][j] = numbers[index]
            matrix[j][i] = numbers[index]
            matrix[n-1-i][n-1-j] = numbers[index]
            matrix[n-1-j][n-1-i] = numbers[index]
            index += 1
    
    # Check if the constructed matrix is palindromic
    if is_palindromic(matrix):
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

solve()