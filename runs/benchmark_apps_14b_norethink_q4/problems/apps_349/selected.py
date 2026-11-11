import sys

def is_possible_to_make_increasing(n, m, matrix1, matrix2):
    def is_strictly_increasing(seq):
        return all(x < y for x, y in zip(seq, seq[1:]))

    for i in range(n):
        combined_row = sorted(matrix1[i] + matrix2[i])
        if not is_strictly_increasing(combined_row[:m]) or not is_strictly_increasing(combined_row[m:]):
            return "Impossible"

    for j in range(m):
        combined_col = sorted([matrix1[i][j] for i in range(n)] + [matrix2[i][j] for i in range(n)])
        if not is_strictly_increasing(combined_col[:n]) or not is_strictly_increasing(combined_col[n:]):
            return "Impossible"

    return "Possible"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    matrix1 = []
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        matrix1.append(row)
        index += m
    
    matrix2 = []
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        matrix2.append(row)
        index += m
    
    result = is_possible_to_make_increasing(n, m, matrix1, matrix2)
    print(result)

if __name__ == "__main__":
    main()