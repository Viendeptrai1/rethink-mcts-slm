import sys

def can_dodge_ships(n, m, ships):
    # Sort ships by y-coordinate
    ships.sort(key=lambda x: x[2])
    
    # Initialize the positions the torpedo can be at after each second
    positions = {0}
    
    for x1, x2, y in ships:
        new_positions = set()
        for pos in positions:
            # Check all possible moves: left, straight, right
            for dx in [-1, 0, 1]:
                new_pos = pos + dx
                if new_pos >= x1 and new_pos <= x2:
                    break
            else:
                new_positions.add(pos + dx)
        
        if not new_positions:
            return "impossible"
        
        positions = new_positions
    
    # Construct the path
    path = []
    current_pos = 0
    for i in range(n):
        for dx in [-1, 0, 1]:
            if current_pos + dx in positions:
                current_pos += dx
                if dx == -1:
                    path.append('-')
                elif dx == 0:
                    path.append('0')
                else:
                    path.append('+')
                break
    
    return ''.join(path)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

ships = []
index = 2
for _ in range(m):
    x1 = int(data[index])
    x2 = int(data[index + 1])
    y = int(data[index + 2])
    ships.append((x1, x2, y))
    index += 3

# Output the result
result = can_dodge_ships(n, m, ships)
print(result)