import sys
from collections import Counter

def is_palindromic_matrix_possible(n, numbers):
    # Check if the number of elements is n^2
    if len(numbers) != n * n:
        return "NO"
    
    # Count the frequency of each number
    count = Counter(numbers)
    
    # Check if each number can be placed symmetrically
    for freq in count.values():
        if freq % 2 != 0:
            return "NO"
    
    # Create the matrix
    matrix = [[0] * n for _ in range(n)]
    
    # Fill the matrix
    num_index = 0
    for i in range(n):
        for j in range(n):
            if i <= j:
                matrix[i][j] = numbers[num_index]
                matrix[j][i] = numbers[num_index]
                num_index += 1
    
    # Check if the matrix is palindromic
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[n-1-i][j] or matrix[i][j] != matrix[i][n-1-j]:
                return "NO"
    
    return "YES", matrix

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    
    result, matrix = is_palindromic_matrix_possible(n, numbers)
    
    if result == "NO":
        print("NO")
    else:
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()