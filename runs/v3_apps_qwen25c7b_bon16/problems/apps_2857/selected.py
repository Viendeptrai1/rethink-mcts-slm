def count_right_triangles(N, points):
    x_count = {}
    y_count = {}
    
    # Count occurrences of each x and y coordinate
    for x, y in points:
        if x in x_count:
            x_count[x] += 1
        else:
            x_count[x] = 1
            
        if y in y_count:
            y_count[y] += 1
        else:
            y_count[y] = 1
    
    # Calculate the number of right triangles
    triangles = 0
    for (x, x_freq) in x_count.items():
        for (y, y_freq) in y_count.items():
            triangles += x_freq * y_freq - x_freq * y_freq * (x_freq + y_freq - 1)
    
    return triangles // 2

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
points = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(N)]

print(count_right_triangles(N, points))