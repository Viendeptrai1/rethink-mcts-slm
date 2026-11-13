def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    grid = [[int(data[i * 3 + j]) for j in range(3)] for i in range(3)]
    
    # Set of possible values for a_i and b_j
    possible_a = set()
    possible_b = set()
    
    # Collect all unique values of a_i from c_{i,1} + b_1 to c_{i,3} + b_3
    for i in range(3):
        for b in range(3):
            possible_a.add(grid[i][b])
    
    # Collect all unique values of b_j from a_1 + c_{1,j} to a_3 + c_{3,j}
    for j in range(3):
        for a in range(3):
            possible_b.add(grid[a][j])
    
    # Check if all values from a_1 to a_3 are in possible_a
    # and all values from b_1 to b_3 are in possible_b
    if len(possible_a) == 3 and len(possible_b) == 3:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()