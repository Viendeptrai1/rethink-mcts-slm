def is_cool(A, r, s, r1, s1, r2, s2):
    """Check if the submatrix defined by (r1, s1) to (r2, s2) is cool."""
    return A[r1][s1] + A[r2][s2] <= A[r1][s2] + A[r2][s1]

def largest_extremely_cool_submatrix(R, S, matrix):
    max_elements = 0

    # Iterate over all possible submatrices with at least 2 rows and 2 columns
    for r1 in range(R):
        for s1 in range(S):
            for r2 in range(r1 + 1, R):
                for s2 in range(s1 + 1, S):
                    # Check if the current submatrix is cool
                    if is_cool(matrix, r1, s1, r2, s2, r1, s2) and is_cool(matrix, r1, s1, r2, s2, r2, s1):
                        # Calculate the number of elements in this submatrix
                        num_elements = (r2 - r1 + 1) * (s2 - s1 + 1)
                        # Update the maximum number of elements found
                        max_elements = max(max_elements, num_elements)

    return max_elements

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    S = int(data[1])
    matrix = []
    
    index = 2
    for _ in range(R):
        row = list(map(int, data[index:index + S]))
        matrix.append(row)
        index += S
    
    result = largest_extremely_cool_submatrix(R, S, matrix)
    print(result)

if __name__ == "__main__":
    main()