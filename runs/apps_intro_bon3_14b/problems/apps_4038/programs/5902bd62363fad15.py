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
    
    # Check if we can form a palindromic matrix
    # We need to check if the numbers can be arranged such that the matrix is palindromic
    # This means that for each number, there should be a corresponding number in the mirrored position
    
    # Create a frequency dictionary
    from collections import Counter
    freq = Counter(numbers)
    
    # Check if all numbers have even frequency except possibly one
    odd_count = sum(1 for count in freq.values() if count % 2 != 0)
    
    if odd_count > 1:
        print("NO")
        return
    
    # If we can form a palindromic matrix, we can just print any valid arrangement
    # For simplicity, we will just print the numbers in a way that forms a palindromic matrix
    # We will fill the matrix row by row, and ensure that the mirrored positions are filled correctly
    
    matrix = [[0] * n for _ in range(n)]
    index = 0
    
    for i in range(n // 2 + 1):
        for j in range(n // 2 + 1):
            if i == n - 1 - i and j == n - 1 - j:
                matrix[i][j] = numbers[index]
                index += 1
            elif i == n - 1 - i:
                matrix[i][j] = numbers[index]
                matrix[i][n - 1 - j] = numbers[index]
                index += 1
            elif j == n - 1 - j:
                matrix[i][j] = numbers[index]
                matrix[n - 1 - i][j] = numbers[index]
                index += 1
            else:
                matrix[i][j] = numbers[index]
                matrix[i][n - 1 - j] = numbers[index]
                matrix[n - 1 - i][j] = numbers[index]
                matrix[n - 1 - i][n - 1 - j] = numbers[index]
                index += 1
    
    if is_palindromic(matrix):
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

solve()