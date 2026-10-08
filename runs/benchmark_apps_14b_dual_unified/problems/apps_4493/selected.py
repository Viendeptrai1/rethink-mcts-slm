import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    # Convert input strings to integers
    c = [[int(data[i*3 + j]) for j in range(3)] for i in range(3)]
    
    # Extract the first row and first column
    first_row = c[0]
    first_col = [c[i][0] for i in range(3)]
    
    # Calculate the differences for rows and columns
    row_diffs = [first_row[j] - first_row[0] for j in range(1, 3)]
    col_diffs = [first_col[i] - first_col[0] for i in range(1, 3)]
    
    # Check if the rest of the grid matches the pattern
    for i in range(1, 3):
        for j in range(1, 3):
            if c[i][j] != first_row[0] + row_diffs[j-1] + first_col[i] - first_col[0]:
                print("No")
                return
    
    print("Yes")

if __name__ == "__main__":
    main()