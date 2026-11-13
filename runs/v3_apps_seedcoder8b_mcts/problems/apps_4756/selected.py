def minimize_unusefulness():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    x_coords = []
    y_coords = []
    
    index = 1
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        x_coords.append(x)
        y_coords.append(y)
        index += 2
    
    x_coords.sort()
    y_coords.sort()
    
    # Calculate the median of x and y coordinates
    if N % 2 == 1:
        median_x = x_coords[N // 2]
        median_y = y_coords[N // 2]
    else:
        median_x = (x_coords[N // 2 - 1] + x_coords[N // 2]) / 2
        median_y = (y_coords[N // 2 - 1] + y_coords[N // 2]) / 2
    
    # The optimal a is the median of y coordinates
    a = median_y
    
    print(f"{a:.6f}")