import sys
from collections import defaultdict

def count_right_triangles(points):
    x_count = defaultdict(int)
    y_count = defaultdict(int)
    
    for x, y in points:
        x_count[x] += 1
        y_count[y] += 1
    
    num_triangles = 0
    for x, y in points:
        # Number of points with the same x-coordinate
        same_x = x_count[x] - 1
        # Number of points with the same y-coordinate
        same_y = y_count[y] - 1
        
        # Calculate the number of right triangles
        num_triangles += same_x * same_y
    
    return num_triangles

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = []
    index = 1
    for i in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        points.append((x, y))
        index += 2
    
    result = count_right_triangles(points)
    print(result)

if __name__ == "__main__":
    main()