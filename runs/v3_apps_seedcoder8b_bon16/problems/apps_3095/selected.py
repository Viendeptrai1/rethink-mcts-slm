import sys

def solve(R, S, matrix):
    def is_cool(r1, c1, r2, c2):
        return (matrix[r1][c1] + matrix[r2][c2] <= 
                matrix[r1][c2] + matrix[r2][c1])

    max_elements = 0
    for r1 in range(R):
        for c1 in range(S):
            for r2 in range(r1 + 1, R):
                for c2 in range(c1 + 1, S):
                    if is_cool(r1, c1, r2, c2):
                        max_elements = max(max_elements, (r2 - r1 + 1) * (c2 - c1 + 1))
                    else:
                        break

    return max_elements

def main():
    R, S = map(int, input().split())
    matrix = [list(map(int, input().split())) for _ in range(R)]
    result = solve(R, S, matrix)
    print(result)

if __name__ == "__main__":
    main()