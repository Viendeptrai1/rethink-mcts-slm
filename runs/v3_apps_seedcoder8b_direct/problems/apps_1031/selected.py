def print_cardiogram(n, sequence):
    # Calculate the sum of the sequence
    total_sum = sum(sequence)
    
    # Calculate the maximum y-coordinate
    max_y = sum((-1) ** (i + 1) * a for i, a in enumerate(sequence))
    
    # Initialize the cardiogram grid
    cardiogram = [[' ' for _ in range(total_sum)] for _ in range(abs(max_y) + 1)]
    
    # Calculate the points of the polyline
    x, y = 0, 0
    cardiogram[-y][x] = '/' if y >= 0 else '\\'
    
    for i, a in enumerate(sequence):
        if i % 2 == 0:
            # Moving up
            for _ in range(a):
                y += 1
                x += 1
                cardiogram[-y][x] = '/'
        else:
            # Moving down
            for _ in range(a):
                y -= 1
                x += 1
                cardiogram[-y][x] = '\\'
    
    # Print the cardiogram
    for line in cardiogram:
        print(''.join(line))

# Read input
n = int(input())
sequence = list(map(int, input().split()))

# Call the function
print_cardiogram(n, sequence)