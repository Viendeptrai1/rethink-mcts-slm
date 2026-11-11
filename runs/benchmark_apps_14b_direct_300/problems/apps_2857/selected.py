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
        # Number of ways to choose another point on the same x-coordinate
        same_x = x_count[x] - 1
        # Number of ways to choose another point on the same y-coordinate
        same_y = y_count[y] - 1
        
        # Each combination of (same_x, same_y) forms a right triangle
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