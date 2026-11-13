def count_right_triangles():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = []
    
    index = 1
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        points.append((x, y))
        index += 2
    
    x_count = {}
    y_count = {}
    
    for x, y in points:
        if x in x_count:
            x_count[x] += 1
        else:
            x_count[x] = 1
        
        if y in y_count:
            y_count[y] += 1
        else:
            y_count[y] = 1
    
    triangles = 0
    
    for x, y in points:
        if x_count[x] > 1 and y_count[y] > 1:
            triangles += (x_count[x] - 1) * (y_count[y] - 1)
    
    print(triangles)