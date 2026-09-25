import sys

def is_palindromic(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[n-1-i][j] or matrix[i][j] != matrix[i][n-1-j]:
                return False
    return True

def find_palindromic_matrix(n, numbers):
    if n % 2 == 0:
        half = n // 2
        top_left = numbers[:half * half]
        top_right = numbers[half * half:2 * half * half]
        bottom_right = numbers[2 * half * half:3 * half * half]
        bottom_left = numbers[3 * half * half:]
        
        matrix = [[0] * n for _ in range(n)]
        idx = 0
        for i in range(half):
            for j in range(half):
                matrix[i][j] = top_left[idx]
                matrix[i][n-1-j] = top_right[idx]
                matrix[n-1-i][j] = bottom_left[idx]
                matrix[n-1-i][n-1-j] = bottom_right[idx]
                idx += 1
        
        if is_palindromic(matrix):
            return matrix
        else:
            return None
    else:
        half = n // 2
        center = numbers[half * half]
        top_left = numbers[:half * half]
        top_right = numbers[half * half + 1:2 * half * half + 1]
        bottom_right = numbers[2 * half * half + 1:3 * half * half + 1]
        bottom_left = numbers[3 * half * half + 1:]
        
        matrix = [[0] * n for _ in range(n)]
        idx = 0
        for i in range(half):
            for j in range(half):
                matrix[i][j] = top_left[idx]
                matrix[i][n-1-j] = top_right[idx]
                matrix[n-1-i][j] = bottom_left[idx]
                matrix[n-1-i][n-1-j] = bottom_right[idx]
                idx += 1
        matrix[half][half] = center
        
        if is_palindromic(matrix):
            return matrix
        else:
            return None

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    
    matrix = find_palindromic_matrix(n, numbers)
    
    if matrix:
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

if __name__ == "__main__":
    main()