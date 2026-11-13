def avoid_ships(n, m, ships):
    # Create a set to store all ship positions
    ship_positions = set()
    for x1, x2, y in ships:
        for x in range(x1, x2 + 1):
            ship_positions.add((x, y))
    
    # Initialize the torpedo's path
    path = ['0'] * n
    x, y = 0, 0
    
    for t in range(n):
        # Check if the torpedo is at a ship's position
        if (x, y) in ship_positions:
            return "impossible"
        
        # Move the torpedo
        if t < n - 1:
            # Decide the next move
            if x > 0 and (x - 1, y + 1) not in ship_positions:
                path[t] = '-'
                x -= 1
            elif x < 0 and (x + 1, y + 1) not in ship_positions:
                path[t] = '+'
                x += 1
            # If neither left nor right move is safe, stay in place
            # This is implicitly handled by '0'
        
        y += 1
    
    return ''.join(path)

# Read input
n, m = map(int, input().split())
ships = [tuple(map(int, input().split())) for _ in range(m)]

# Solve and print result
result = avoid_ships(n, m, ships)
print(result)