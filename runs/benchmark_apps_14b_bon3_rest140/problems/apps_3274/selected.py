import sys

def can_dodge_torpedo(n, m, ships):
    # Sort ships by y-coordinate
    ships.sort(key=lambda x: x[2])
    
    # Initialize the set of positions the torpedo can be in
    current_positions = {0}
    
    for x1, x2, y in ships:
        next_positions = set()
        for pos in current_positions:
            # Check all possible moves: left, straight, right
            for dx in [-1, 0, 1]:
                new_pos = pos + dx
                if x1 <= new_pos <= x2:
                    break
            else:
                next_positions.add(pos + dx)
        
        if not next_positions:
            return "impossible"
        
        current_positions = next_positions
    
    # Construct the path
    path = []
    current_pos = 0
    for _ in range(n):
        for dx in [-1, 0, 1]:
            new_pos = current_pos + dx
            if new_pos in current_positions:
                path.append('+' if dx == 1 else '-' if dx == -1 else '0')
                current_pos = new_pos
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
result = can_dodge_torpedo(n, m, ships)
print(result)