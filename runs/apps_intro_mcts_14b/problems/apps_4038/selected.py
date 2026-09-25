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
    
    if len(numbers) != n * n:
        print("NO")
        return
    
    # Try to construct a palindromic matrix
    matrix = [[0] * n for _ in range(n)]
    used = set()
    
    def fill_matrix(row, col):
        if row == n:
            return True
        if col == n:
            return fill_matrix(row + 1, 0)
        
        if matrix[row][col] != 0:
            return fill_matrix(row, col + 1)
        
        for num in numbers:
            if num not in used:
                matrix[row][col] = num
                matrix[n-1-row][n-1-col] = num
                used.add(num)
                
                if fill_matrix(row, col + 1):
                    return True
                
                matrix[row][col] = 0
                matrix[n-1-row][n-1-col] = 0
                used.remove(num)
        
        return False
    
    if fill_matrix(0, 0):
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

if __name__ == "__main__":
    solve()