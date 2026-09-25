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
    
    matrix = [[0] * n for _ in range(n)]
    used = set()
    
    def place_numbers(row, col):
        if row == n // 2 and col == n // 2 and n % 2 == 1:
            for num in numbers:
                if num not in used:
                    matrix[row][col] = num
                    used.add(num)
                    break
            return is_palindromic(matrix)
        
        if row >= n or col >= n:
            return False
        
        if matrix[row][col] != 0:
            return place_numbers(row + (col == n - 1), (col + 1) % n)
        
        for num in numbers:
            if num not in used:
                matrix[row][col] = num
                matrix[row][n-1-col] = num
                matrix[n-1-row][col] = num
                matrix[n-1-row][n-1-col] = num
                used.add(num)
                
                if place_numbers(row + (col == n - 1), (col + 1) % n):
                    return True
                
                used.remove(num)
                matrix[row][col] = 0
                matrix[row][n-1-col] = 0
                matrix[n-1-row][col] = 0
                matrix[n-1-row][n-1-col] = 0
        
        return False
    
    if place_numbers(0, 0):
        print("YES")
        for row in matrix:
            print(" ".join(map(str, row)))
    else:
        print("NO")

if __name__ == "__main__":
    solve()