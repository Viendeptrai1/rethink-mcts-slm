import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    x1, y1, x2, y2 = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    
    # Calculate the vector from (x1, y1) to (x2, y2)
    dx, dy = x2 - x1, y2 - y1
    
    # Calculate the other two vertices
    x3, y3 = x2 - dy, y2 + dx
    x4, y4 = x1 - dy, y1 + dx
    
    print(x3, y3, x4, y4)

if __name__ == "__main__":
    main()