def max_elements_in_extremely_cool_submatrix(R, S, matrix):
    def is_cool(submatrix):
        r, s = len(submatrix), len(submatrix[0])
        return submatrix[0][0] + submatrix[r-1][s-1] <= submatrix[0][s-1] + submatrix[r-1][0]

    max_size = 0
    for i in range(R):
        for j in range(S):
            for k in range(i+1, R+1):
                for l in range(j+1, S+1):
                    submatrix = [row[j:l] for row in matrix[i:k]]
                    if is_cool(submatrix):
                        max_size = max(max_size, (k-i)*(l-j))
    
    return max_size

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
R = int(data[0])
S = int(data[1])
matrix = [[int(data[2+i*S+j]) for j in range(S)] for i in range(R)]
print(max_elements_in_extremely_cool_submatrix(R, S, matrix))