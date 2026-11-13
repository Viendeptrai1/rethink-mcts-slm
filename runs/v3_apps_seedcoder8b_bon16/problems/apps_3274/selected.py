def avoid_ships(n, m, ships):
    # We'll try to construct the path for the torpedo
    # Torpedo starts at (0,0) and tries to move towards the maximum y value
    # We aim to avoid collisions by moving either left, right or staying still
    path = ['0'] * n
    
    # Sort ships by their y-value to process in the order they appear in the y-axis
    ships.sort(key=lambda ship: ship[2])
    
    # Iterate through each ship and decide the path step by step
    for i in range(m):
        x1, x2, y = ships[i]
        
        # Calculate if the torpedo can reach and hit this ship
        # Torpedo will move from (0,0) to (0,y), then (x,y) to (x,y+n)
        if y <= n:
            # Calculate the horizontal distance from the torpedo to the ship's x-range
            # At time y, the torpedo is at (0,y), so we need to ensure that it doesn't overlap with x1 to x2 at time y+n
            if 0 <= x1 <= x2 <= n:
                return "impossible"
    
    # If we have processed all ships and found no immediate collision
    # We can safely assume it's possible to avoid them all
    return ''.join(path)

import sys
input = sys.stdin.read

def main():
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
    
    result = avoid_ships(n, m, ships)
    print(result)

if __name__ == "__main__":
    main()