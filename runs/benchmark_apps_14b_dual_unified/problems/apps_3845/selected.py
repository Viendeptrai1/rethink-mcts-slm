import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    A = int(data[0])
    B = int(data[1])
    
    # Calculate the minimum grid size needed
    h = max(A, B)
    w = A + B
    
    # Create the grid
    grid = [['.' for _ in range(w)] for _ in range(h)]
    
    # Fill the grid with A connected white components
    for i in range(A):
        grid[i][i] = '.'
    
    # Fill the grid with B connected black components
    for i in range(B):
        grid[h-1-i][w-1-i] = '#'
    
    # Print the grid size
    print(h, w)
    
    # Print the grid
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    main()