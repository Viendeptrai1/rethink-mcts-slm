def avoid_ships(n, m, ships):
    # Create a set to store all ship positions
    ship_positions = set()
    for x1, x2, y in ships:
        for x in range(x1, x2 + 1):
            ship_positions.add((x, y))
    
    # Initialize the torpedo's position
    torpedo_x, torpedo_y = 0, 0
    
    # Create a list to store the instructions
    instructions = []
    
    # Simulate the torpedo's movement
    for _ in range(n):
        # Check if the torpedo is on a ship
        if (torpedo_x, torpedo_y) in ship_positions:
            return "impossible"
        
        # Decide the next move
        if torpedo_y + 1 < n:
            # Check if we can move forward
            if (torpedo_x, torpedo_y + 1) not in ship_positions:
                instructions.append('0')
                torpedo_y += 1
            elif torpedo_x - 1 >= -n and (torpedo_x - 1, torpedo_y + 1) not in ship_positions:
                instructions.append('-')
                torpedo_x -= 1
                torpedo_y += 1
            elif torpedo_x + 1 <= n and (torpedo_x + 1, torpedo_y + 1) not in ship_positions:
                instructions.append('+')
                torpedo_x += 1
                torpedo_y += 1
            else:
                return "impossible"
        else:
            # We've reached the maximum y-coordinate
            instructions.append('0')
    
    return ''.join(instructions)

# Read input
n, m = map(int, input().split())
ships = [tuple(map(int, input().split())) for _ in range(m)]

# Call the function and print the result
result = avoid_ships(n, m, ships)
print(result)