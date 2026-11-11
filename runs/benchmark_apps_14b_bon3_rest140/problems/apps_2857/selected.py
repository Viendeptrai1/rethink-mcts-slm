import sys
from collections import defaultdict

def count_right_triangles(N, points):
    x_count = defaultdict(int)
    y_count = defaultdict(int)
    
    for x, y in points:
        x_count[x] += 1
        y_count[y] += 1
    
    count = 0
    for x, y in points:
        # Number of points with the same x-coordinate (excluding the current point)
        same_x = x_count[x] - 1
        # Number of points with the same y-coordinate (excluding the current point)
        same_y = y_count[y] - 1
        
        # Each combination of same_x and same_y forms a right triangle with the current point
        count += same_x * same_y
    
    return count

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
    
    result = count_right_triangles(N, points)
    print(result)

if __name__ == "__main__":
    main()