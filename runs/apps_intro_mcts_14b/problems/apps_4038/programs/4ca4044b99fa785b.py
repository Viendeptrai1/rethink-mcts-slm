import sys

def is_palindromic_matrix_possible(n, numbers):
    # Check if the number of elements is correct
    if len(numbers) != n * n:
        return "NO"
    
    # Sort the numbers to facilitate pairing
    numbers.sort()
    
    # Create a dictionary to count occurrences of each number
    count = {}
    for num in numbers:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1
    
    # Check if each number can be paired symmetrically
    for num in count:
        if count[num] % 2 != 0:
            return "NO"
    
    # Construct the matrix
    matrix = [[0] * n for _ in range(n)]
    
    # Fill the matrix symmetrically
    index = 0
    for i in range(n):
        for j in range(i, n - i):
            if i == j or i + j == n - 1:
                matrix[i][j] = numbers[index]
                index += 1
            else:
                matrix[i][j] = numbers[index]
                matrix[j][i] = numbers[index]
                matrix[n-i-1][j] = numbers[index]
                matrix[j][n-i-1] = numbers[index]
                index += 1
    
    return "YES", matrix

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    
    result, matrix = is_palindromic_matrix_possible(n, numbers)
    
    print(result)
    if result == "YES":
        for row in matrix:
            print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()