import sys

def read_input():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    matrix = []
    index = 2
    for i in range(n):
        row = list(map(int, data[index:index + m]))
        matrix.append(row)
        index += m
    return n, m, matrix

def is_mirror(matrix, n, m):
    for i in range(n // 2):
        for j in range(m):
            if matrix[i][j] != matrix[n - i - 1][j]:
                return False
    return True

def find_min_rows(n, m, matrix):
    if n % 2 == 0 and is_mirror(matrix, n, m):
        return n // 2
    else:
        return n

def main():
    n, m, matrix = read_input()
    result = find_min_rows(n, m, matrix)
    print(result)

if __name__ == "__main__":
    main()