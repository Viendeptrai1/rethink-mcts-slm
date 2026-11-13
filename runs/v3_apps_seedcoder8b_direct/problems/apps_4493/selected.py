def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    # Parse the input into a 3x3 grid
    grid = [[int(data[i * 3 + j]) for j in range(3)] for i in range(3)]
    
    # Check all possible combinations of a_i and b_j
    for a1 in range(101):
        for a2 in range(101):
            for a3 in range(101):
                for b1 in range(101):
                    for b2 in range(101):
                        for b3 in range(101):
                            # Check if the grid matches the condition
                            if (grid[0][0] == a1 + b1 and grid[0][1] == a1 + b2 and grid[0][2] == a1 + b3 and
                                grid[1][0] == a2 + b1 and grid[1][1] == a2 + b2 and grid[1][2] == a2 + b3 and
                                grid[2][0] == a3 + b1 and grid[2][1] == a3 + b2 and grid[2][2] == a3 + b3):
                                print("Yes")
                                return
    print("No")

if __name__ == "__main__":
    main()