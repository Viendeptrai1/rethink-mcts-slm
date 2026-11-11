import sys

def main():
    # Read the input grid
    grid = []
    for _ in range(3):
        row = list(map(int, sys.stdin.readline().split()))
        grid.append(row)
    
    # Extract the values
    c11, c12, c13 = grid[0]
    c21, c22, c23 = grid[1]
    c31, c32, c33 = grid[2]
    
    # Check if the grid can be represented as a_i + b_j
    a1 = c11
    a2 = c21 - c11
    a3 = c31 - c11
    
    b1 = c11 - a1
    b2 = c12 - a1
    b3 = c13 - a1
    
    # Verify the values
    if (a1 + b1 == c11 and a1 + b2 == c12 and a1 + b3 == c13 and
        a2 + b1 == c21 and a2 + b2 == c22 and a2 + b3 == c23 and
        a3 + b1 == c31 and a3 + b2 == c32 and a3 + b3 == c33):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()