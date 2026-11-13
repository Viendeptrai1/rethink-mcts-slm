def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    # Parse the input into a 3x3 grid
    grid = [[int(data[i * 3 + j]) for j in range(3)] for i in range(3)]
    
    # Calculate the sums of the rows and columns
    row_sums = [sum(grid[i]) for i in range(3)]
    col_sums = [sum(grid[i][j] for i in range(3)) for j in range(3)]
    
    # Check if all row sums are equal
    if not all(x == row_sums[0] for x in row_sums):
        print("No")
        return
    
    # Check if all column sums are equal
    if not all(x == col_sums[0] for x in col_sums):
        print("No")
        return
    
    # If both row and column sums are equal, Takahashi's statement is correct
    print("Yes")

if __name__ == "__main__":
    main()