import sys

def paint_cardiogram(n, a):
    # Calculate the coordinates of the cardiogram
    x_coords = [0]
    y_coords = [0]
    for i in range(n):
        x_coords.append(x_coords[-1] + a[i])
        y_coords.append(y_coords[-1] + (-1)**(i+1) * a[i])
    
    # Determine the bounding box of the cardiogram
    min_y = min(y_coords)
    max_y = max(y_coords)
    total_width = x_coords[-1]
    
    # Function to determine if a point (x, y) is on the cardiogram
    def is_on_cardiogram(x, y):
        for i in range(n):
            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[i+1], y_coords[i+1]
            if (y - y1) * (x2 - x1) == (y2 - y1) * (x - x1):
                return True
        return False
    
    # Print the cardiogram
    for y in range(max_y, min_y - 1, -1):
        line = [' '] * total_width
        for x in range(total_width):
            if is_on_cardiogram(x, y):
                if y_coords[x_coords.index(x)] > y_coords[x_coords.index(x) + 1]:
                    line[x] = '/'
                else:
                    line[x] = '\\'
        print(''.join(line))

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Paint the cardiogram
paint_cardiogram(n, a)