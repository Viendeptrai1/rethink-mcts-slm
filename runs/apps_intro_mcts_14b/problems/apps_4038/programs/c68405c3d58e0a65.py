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
    
    if len(numbers) != n * n:
        print("NO")
        return
    
    # Check if we can form a palindromic matrix
    if n % 2 == 0:
        # Even n, we need pairs of numbers
        from collections import Counter
        count = Counter(numbers)
        for v in count.values():
            if v % 2 != 0:
                print("NO")
                return
    else:
        # Odd n, we need pairs of numbers and one middle number
        from collections import Counter
        count = Counter(numbers)
        odd_count = sum(1 for v in count.values() if v % 2 != 0)
        if odd_count > 1:
            print("NO")
            return
    
    # Create the matrix
    matrix = [[0] * n for _ in range(n)]
    
    # Fill the top-left quadrant
    idx = 0
    for i in range((n + 1) // 2):
        for j in range((n + 1) // 2):
            matrix[i][j] = numbers[idx]
            idx += 1
    
    # Fill the bottom-right quadrant based on top-left
    for i in range((n + 1) // 2):
        for j in range((n + 1) // 2):
            matrix[n - 1 - i][n - 1 - j] = matrix[i][j]
    
    # Fill the top-right quadrant based on bottom-left
    for i in range((n + 1) // 2):
        for j in range((n + 1) // 2):
            matrix[i][n - 1 - j] = matrix[n - 1 - i][j]
    
    # Fill the bottom-left quadrant based on top-right
    for i in range((n + 1) // 2):
        for j in range((n + 1) // 2):
            matrix[n - 1 - i][j] = matrix[i][n - 1 - j]
    
    # Check if the matrix is palindromic
    if is_palindromic(matrix):
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

solve()