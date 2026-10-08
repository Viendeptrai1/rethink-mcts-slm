import sys

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    m = int(data[1])
    matrix = []
    index = 2
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        matrix.append(row)
        index += m
    return n, m, matrix

def is_symmetric(matrix, n, m):
    for i in range(n // 2):
        for j in range(m):
            if matrix[i][j] != matrix[n - i - 1][j]:
                return False
    return True

def min_rows_for_b(n, m, matrix):
    if is_symmetric(matrix, n, m):
        return (n + 1) // 2
    else:
        return n

def main():
    n, m, matrix = read_input()
    result = min_rows_for_b(n, m, matrix)
    print(result)

if __name__ == "__main__":
    main()