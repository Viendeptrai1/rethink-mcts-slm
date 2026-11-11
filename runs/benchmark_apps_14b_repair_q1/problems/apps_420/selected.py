import sys

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    return data

def main():
    data = read_input()
    index = 0
    n = int(data[index])
    index += 1
    m = int(data[index])
    index += 1
    matrix_a = []
    for i in range(n):
        row = list(map(int, data[index:index + m]))
        index += m
        matrix_a.append(row)
    
    def is_symmetric(matrix, x):
        for i in range(x):
            for j in range(m):
                if matrix[i][j] != matrix[2 * x - i - 1][j]:
                    return False
        return True
    
    for x in range(1, n + 1):
        if is_symmetric(matrix_a, x):
            print(x)
            return

if __name__ == "__main__":
    main()