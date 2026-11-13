import sys

def max_elements_in_extremely_cool_submatrix(R, S, matrix):
    def is_cool(submatrix):
        r = len(submatrix)
        s = len(submatrix[0])
        return all(submatrix[0][0] + submatrix[r-1][s-1] <= submatrix[i][s-1] + submatrix[0][i] for i in range(1, s))

    max_elements = 0
    for i in range(R):
        for j in range(S):
            for k in range(i+1, R):
                for l in range(j+1, S):
                    submatrix = [row[j:l] for row in matrix[i:k]]
                    if is_cool(submatrix):
                        max_elements = max(max_elements, (k-i)*(l-j))
    return max_elements

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    S = int(data[1])
    matrix = [[int(data[2+i*S+j]) for j in range(S)] for i in range(R)]
    
    result = max_elements_in_extremely_cool_submatrix(R, S, matrix)
    print(result)