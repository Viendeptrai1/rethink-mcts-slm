import sys

def dodge_ships(n, m, ships):
    # Sort ships by their starting x-coordinate
    ships.sort(key=lambda x: x[0])
    
    # Initialize the current position of the torpedo
    x, y = 0, 0
    
    # Initialize the result list
    result = []
    
    # Iterate through each second until the torpedo runs out of fuel
    for t in range(n):
        found_path = False
        
        # Check all possible moves
        for dx in [-1, 0, 1]:
            nx, ny = x + dx, y + 1
            
            # Check if the move is valid
            if nx <= n and ny > 0 and ny <= n:
                valid_move = True
                
                # Check if the move intersects with any ship
                for sx1, sx2, sy in ships:
                    if sy == ny:
                        if nx >= sx1 and nx <= sx2:
                            valid_move = False
                            break
                
                # If the move is valid, update the position and add to result
                if valid_move:
                    x, y = nx, ny
                    result.append('+' if dx == 1 else '-' if dx == -1 else '0')
                    found_path = True
                    break
        
        # If no valid move was found, return "impossible"
        if not found_path:
            return "impossible"
    
    # Join the result list into a string and return
    return ''.join(result)

# Read input from stdin
input = sys.stdin.read
data = input().split()

# Parse the input
n = int(data[0])
m = int(data[1])

ships = []
index = 2
for i in range(m):
    x1 = int(data[index])
    x2 = int(data[index + 1])
    y = int(data[index + 2])
    ships.append((x1, x2, y))
    index += 3

# Call the function and print the result
result = dodge_ships(n, m, ships)
print(result)