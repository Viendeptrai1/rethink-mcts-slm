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
    
    # If we reach here, we can form a palindromic matrix
    print("YES")
    matrix = [[0] * n for _ in range(n)]
    idx = 0
    for i in range(n // 2 + 1):
        for j in range(n // 2 + 1):
            matrix[i][j] = numbers[idx]
            matrix[i][n-1-j] = numbers[idx]
            matrix[n-1-i][j] = numbers[idx]
            matrix[n-1-i][n-1-j] = numbers[idx]
            idx += 1
    
    for row in matrix:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    solve()