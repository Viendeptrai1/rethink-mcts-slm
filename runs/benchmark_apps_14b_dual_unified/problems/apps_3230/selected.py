import heapq
from collections import defaultdict

def calculate_explosions(R, C, tram):
    # Directions for moving up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Priority queue to store (distance, row, col) tuples
    pq = []
    
    # Dictionary to store the closest seat for each passenger
    closest_seat = {}
    
    # Find all passengers and add them to the priority queue
    for r in range(R):
        for c in range(C):
            if tram[r][c] == 'X':
                # Calculate initial distances to all seats
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < R and 0 <= nc < C:
                        if tram[nr][nc] == 'L':
                            distance = ((nr - r) ** 2 + (nc - c) ** 2) ** 0.5
                            heapq.heappush(pq, (distance, nr, nc, r, c))
                            break
                        elif tram[nr][nc] != '.':
                            break
                        nr += dr
                        nc += dc
    
    # Process the priority queue
    explosions = 0
    seated_passengers = set()
    
    while pq:
        distance, sr, sc, pr, pc = heapq.heappop(pq)
        
        # If the passenger is already seated, skip
        if (pr, pc) in seated_passengers:
            continue
        
        # Check if the seat is already taken
        if (sr, sc) in closest_seat:
            # If another passenger is already closest to this seat, it's an explosion
            if closest_seat[(sr, sc)] != (pr, pc):
                explosions += 1
            else:
                # Otherwise, seat the passenger
                seated_passengers.add((pr, pc))
        else:
            # Seat the passenger
            closest_seat[(sr, sc)] = (pr, pc)
            seated_passengers.add((pr, pc))
    
    return explosions

# Read input
import sys
input = sys.stdin.read
data = input().split()

R = int(data[0])
C = int(data[1])
tram = data[2:]

# Calculate and print the number of explosions
print(calculate_explosions(R, C, tram))