def cardiogram(n, a):
    x = 0
    y = 0
    points = [(x, y)]
    
    for i in range(n):
        if i % 2 == 0:
            y += a[i]
        else:
            y -= a[i]
        x += a[i]
        points.append((x, y))
    
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)
    max_height = max_y - min_y + 1
    width = x + 1
    
    canvas = [[' ' for _ in range(width)] for _ in range(max_height)]
    
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        if y1 == y2:
            continue
        
        if y1 < y2:
            for x in range(x1, x2):
                canvas[y2 - y][x] = '/'
        else:
            for x in range(x1, x2):
                canvas[y1 - y][x] = '\\'
    
    for row in canvas:
        print(''.join(row))

# Read input
n = int(input())
a = list(map(int, input().split()))

# Call the function
cardiogram(n, a)