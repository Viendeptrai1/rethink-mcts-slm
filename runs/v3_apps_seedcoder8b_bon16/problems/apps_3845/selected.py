def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    A = int(data[0])
    B = int(data[1])
    
    # Construct the grid based on A and B
    grid = []
    
    def create_connected_components(size, count):
        components = []
        current = []
        for i in range(size):
            for j in range(size):
                current.append((i, j))
                if len(current) == size:
                    components.append(current)
                    current = []
        while len(components) < count:
            # Merge two components to create a new one
            if len(components) >= 2:
                c1 = components.pop()
                c2 = components.pop()
                new_component = c1 + c2
                components.append(new_component)
            else:
                new_component = components.pop() + [(0, 0)]
                components.append(new_component)
        return components
    
    # Estimate a reasonable size for the grid
    size = int((A + B) ** 0.5) + 1
    white_components = create_connected_components(size, A)
    black_components = create_connected_components(size, B)
    
    grid = [['#' for _ in range(size)] for _ in range(size)]
    
    for component in white_components:
        for (x, y) in component:
            grid[x][y] = '.'
    
    for component in black_components:
        for (x, y) in component:
            grid[x][y] = '#'
    
    # Print the grid
    print(size, size)
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    main()