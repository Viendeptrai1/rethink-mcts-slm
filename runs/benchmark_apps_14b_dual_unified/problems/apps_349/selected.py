import sys

def is_increasing(matrix):
    n = len(matrix)
    m = len(matrix[0])
    for i in range(n):
        for j in range(1, m):
            if matrix[i][j] <= matrix[i][j - 1]:
                return False
    for j in range(m):
        for i in range(1, n):
            if matrix[i][j] <= matrix[i - 1][j]:
                return False
    return True

def can_make_increasing(n, m, matrix1, matrix2):
    for i in range(n):
        for j in range(m):
            if matrix1[i][j] > matrix2[i][j]:
                # Try to find a swap that can fix this
                found_swap = False
                for ni in range(n):
                    for nj in range(m):
                        if ni == i and nj == j:
                            continue
                        if matrix1[ni][nj] < matrix2[ni][nj]:
                            # Swap (i, j) and (ni, nj)
                            matrix1[i][j], matrix1[ni][nj] = matrix1[ni][nj], matrix1[i][j]
                            matrix2[i][j], matrix2[ni][nj] = matrix2[ni][nj], matrix2[i][j]
                            if is_increasing(matrix1) and is_increasing(matrix2):
                                return "Possible"
                            # Swap back
                            matrix1[i][j], matrix1[ni][nj] = matrix1[ni][nj], matrix1[i][j]
                            matrix2[i][j], matrix2[ni][nj] = matrix2[ni][nj], matrix2[i][j]
                            found_swap = True
                            break
                    if found_swap:
                        break
                if not found_swap:
                    return "Impossible"
    return "Possible"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    m = int(data[index])
    index += 1
    
    matrix1 = []
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        index += m
        matrix1.append(row)
    
    matrix2 = []
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        index += m
        matrix2.append(row)
    
    result = can_make_increasing(n, m, matrix1, matrix2)
    print(result)

if __name__ == "__main__":
    main()