import sys

def min_rows_for_mirroring(n, m, matrix):
    def is_symmetric(submatrix):
        return submatrix == submatrix[::-1]

    for x in range(1, n + 1):
        upper_half = matrix[:x]
        if is_symmetric(upper_half):
            return x
    return n

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    matrix = []
    
    index = 2
    for i in range(n):
        row = list(map(int, data[index:index + m]))
        matrix.append(row)
        index += m
    
    result = min_rows_for_mirroring(n, m, matrix)
    print(result)

if __name__ == "__main__":
    main()