import sys

def restore_square_vertices(x1, y1, x2, y2):
    # Calculate the vector from (x1, y1) to (x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    
    # Calculate the other two vertices (x3, y3) and (x4, y4)
    x3 = x1 - dy
    y3 = y1 + dx
    x4 = x2 - dy
    y4 = y2 + dx
    
    return x3, y3, x4, y4

def main():
    # Read input from standard input
    input = sys.stdin.read().strip()
    x1, y1, x2, y2 = map(int, input.split())
    
    # Restore the square vertices
    x3, y3, x4, y4 = restore_square_vertices(x1, y1, x2, y2)
    
    # Print the result
    print(x3, y3, x4, y4)

if __name__ == "__main__":
    main()