import sys
import math
from collections import defaultdict

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def count_explosions(R, C, tram_layout):
    passengers = []
    seats = []
    
    # Collect positions of passengers and seats
    for r in range(R):
        for c in range(C):
            if tram_layout[r][c] == 'X':
                passengers.append((r, c))
            elif tram_layout[r][c] == 'L':
                seats.append((r, c))
    
    explosions = 0
    
    while passengers:
        passenger_distances = defaultdict(list)
        
        # Calculate distances from each passenger to each seat
        for px, py in passengers:
            for sx, sy in seats:
                distance = calculate_distance(px, py, sx, sy)
                passenger_distances[(px, py)].append((distance, sx, sy))
        
        # Sort distances for each passenger
        for passenger, distances in passenger_distances.items():
            distances.sort()
        
        # Assign seats or mark for explosion
        assigned_seats = set()
        new_passengers = []
        
        for px, py in passengers:
            distances = passenger_distances[(px, py)]
            min_distance, sx, sy = distances[0]
            
            if len(distances) > 1 and distances[1][0] == min_distance:
                explosions += 1
            else:
                if (sx, sy) not in assigned_seats:
                    assigned_seats.add((sx, sy))
                else:
                    explosions += 1
        
        # Filter out passengers who have been seated or exploded
        for px, py in passengers:
            if (px, py) not in passenger_distances or not passenger_distances[(px, py)]:
                continue
            min_distance, sx, sy = passenger_distances[(px, py)][0]
            if (sx, sy) not in assigned_seats:
                new_passengers.append((px, py))
        
        passengers = new_passengers
    
    return explosions

# Read input
input = sys.stdin.read
data = input().split()

R = int(data[0])
C = int(data[1])
tram_layout = data[2:]

# Calculate and print the number of explosions
print(count_explosions(R, C, tram_layout))