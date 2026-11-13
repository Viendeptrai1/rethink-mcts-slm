def min_rows_for_mirroring(n, m, a):
    def is_symmetric(matrix, rows):
        for i in range(rows):
            if matrix[i] != matrix[rows - i - 1]:
                return False
        return True

    for rows in range(1, n + 1):
        if n % rows == 0:
            if is_symmetric(a, rows):
                return rows
    return n

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = []
    index = 2
    for _ in range(n):
        a.append(list(map(int, data[index:index + m])))
        index += m
    
    result = min_rows_for_mirroring(n, m, a)
    print(result)