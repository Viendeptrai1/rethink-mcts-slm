def print_cardiogram(n, sequence):
    total_sum = sum(sequence)
    max_diff = 0
    y_coords = []
    
    x, y = 0, 0
    y_coords.append(y)
    
    for i in range(n):
        if i % 2 == 0:
            y -= sequence[i]
        else:
            y += sequence[i]
        x += sequence[i]
        y_coords.append(y)
        max_diff = max(max_diff, abs(y))
    
    canvas = [[' ' for _ in range(total_sum)] for _ in range(max_diff + 1)]
    
    x, y = 0, max_diff - y_coords[0]
    for i in range(1, len(y_coords)):
        new_y = max_diff - y_coords[i]
        if new_y > y:
            for j in range(y, new_y):
                canvas[j][x] = '/'
        elif new_y < y:
            for j in range(new_y, y):
                canvas[j][x] = '\\'
        x += sequence[i - 1]
        y = new_y
    
    for line in canvas:
        print(''.join(line))

# Read input
n = int(input())
sequence = list(map(int, input().split()))

# Call the function
print_cardiogram(n, sequence)