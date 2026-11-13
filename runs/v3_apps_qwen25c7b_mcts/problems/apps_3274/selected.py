import sys

def can_dodge(n, m, ships):
    # Sort ships by their y-coordinate
    ships.sort(key=lambda x: x[2])
    
    # Initialize the current position of the torpedo
    x, y = 0, 0
    
    # Initialize the result string
    result = []
    
    for _ in range(n):
        found_path = False
        
        # Try moving right-up, straight up, and left-up
        for dx in [-1, 0, 1]:
            nx, ny = x + dx, y + 1
            
            # Check if the new position is within bounds and does not collide with any ship
            if -n <= nx <= n and 1 <= ny < n:
                valid = True
                for sx1, sx2, sy in ships:
                    if sy == ny and (sx1 <= nx <= sx2):
                        valid = False
                        break
                
                if valid:
                    x, y = nx, ny
                    result.append('+-'[dx > 0] + '0+'[dx == 0] + '-+'[dx < 0])
                    found_path = True
                    break
        
        # If no valid path is found, return "impossible"
        if not found_path:
            return "impossible"
    
    return ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

ships = []
for i in range(m):
    x1 = int(data[2 + 3 * i])
    x2 = int(data[3 + 3 * i])
    y = int(data[4 + 3 * i])
    ships.append((x1, x2, y))

# Solve the problem
result = can_dodge(n, m, ships)
print(result)