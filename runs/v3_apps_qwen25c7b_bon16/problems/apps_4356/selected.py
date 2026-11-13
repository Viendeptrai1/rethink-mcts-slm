def contains_template(A, B):
    N = len(A)
    M = len(B)
    
    def is_submatrix(matrix, submatrix, top_left):
        x, y = top_left
        for i in range(M):
            for j in range(M):
                if matrix[x + i][y + j] != submatrix[i][j]:
                    return False
        return True
    
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            if is_submatrix(A, B, (i, j)):
                return "Yes"
    
    return "No"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    A = data[2:N+2]
    B = data[N+2:N+2+M]
    
    print(contains_template(A, B))