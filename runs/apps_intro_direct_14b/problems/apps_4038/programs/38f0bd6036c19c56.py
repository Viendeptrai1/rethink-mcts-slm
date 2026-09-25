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
    # We need to check if the numbers can be arranged such that the matrix is palindromic
    # This means that for each number, there should be a corresponding number in the mirrored position
    
    # Create a frequency dictionary of the numbers
    from collections import Counter
    freq = Counter(numbers)
    
    # Check if each number has an even count (except for the center element if n is odd)
    for num, count in freq.items():
        if count % 2 != 0:
            if n % 2 == 0 or num != numbers[n*n//2]:
                print("NO")
                return
    
    # If we reach here, it means we can form a palindromic matrix
    print("YES")
    
    # Construct the matrix
    matrix = [[0] * n for _ in range(n)]
    index = 0
    
    # Fill the top-left triangle
    for i in range(n):
        for j in range(i+1):
            matrix[i][j] = numbers[index]
            matrix[j][i] = numbers[index]
            index += 1
    
    # If n is odd, fill the center element
    if n % 2 == 1:
        matrix[n//2][n//2] = numbers[index]
    
    # Print the matrix
    for row in matrix:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    solve()