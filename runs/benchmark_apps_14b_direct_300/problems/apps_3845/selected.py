import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    A = int(data[0])
    B = int(data[1])
    
    # Determine the size of the grid
    h = A + B
    w = 2
    
    # Create the grid
    grid = []
    for i in range(h):
        if i < A:
            grid.append("..")
        else:
            grid.append("#.")
    
    # Print the size of the grid
    print(h, w)
    
    # Print the grid
    for row in grid:
        print(row)

if __name__ == "__main__":
    main()