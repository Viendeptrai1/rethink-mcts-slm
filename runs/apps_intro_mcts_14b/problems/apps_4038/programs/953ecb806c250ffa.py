import sys
from collections import Counter

def is_palindromic(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[n-1-i][j] or matrix[i][j] != matrix[i][n-1-j]:
                return False
    return True

def construct_palindromic_matrix(n, numbers):
    if n == 1:
        return [[numbers[0]]]
    
    # Check if we can pair numbers symmetrically
    count = Counter(numbers)
    for num in count:
        if count[num] % 2 != 0:
            return None
    
    # Create the matrix
    matrix = [[0] * n for _ in range(n)]
    num_index = 0
    
    # Fill the top-left triangle
    for i in range(n // 2 + 1):
        for j in range(i + 1):
            matrix[i][j] = numbers[num_index]
            matrix[j][i] = numbers[num_index]
            if i != j:
                matrix[n-1-i][j] = numbers[num_index]
                matrix[j][n-1-i] = numbers[num_index]
                matrix[i][n-1-j] = numbers[num_index]
                matrix[n-1-j][i] = numbers[num_index]
            num_index += 1
    
    return matrix

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    
    matrix = construct_palindromic_matrix(n, numbers)
    
    if matrix is None:
        print("NO")
    else:
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()