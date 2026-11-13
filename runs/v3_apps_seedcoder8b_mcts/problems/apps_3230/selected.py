import sys
import math
from collections import defaultdict

def count_explosions(R, C, grid):
    # Find all positions of 'X' and 'L'
    passengers = []
    seats = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'X':
                passengers.append((r, c))
            elif grid[r][c] == 'L':
                seats.append((r, c))
    
    # Function to calculate Euclidean distance
    def euclidean_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    # Dictionary to map seats to their closest passengers
    seat_to_passengers = defaultdict(list)
    
    # Assign each passenger to the closest seat
    for passenger in passengers:
        min_distance = float('inf')
        closest_seat = None
        for seat in seats:
            distance = euclidean_distance(passenger, seat)
            if distance < min_distance:
                min_distance = distance
                closest_seat = seat
        seat_to_passengers[closest_seat].append(passenger)
    
    # Count the number of explosions
    explosions = 0
    seated_passengers = set()
    
    for seat, passengers in seat_to_passengers.items():
        if len(passengers) == 1:
            seated_passengers.add(passengers[0])
        else:
            # All passengers are equally close to this seat
            explosions += 1
    
    return explosions

def main():
    input = sys.stdin.read
    data = input().splitlines()
    
    R, C = map(int, data[0].split())
    grid = data[1:R+1]
    
    result = count_explosions(R, C, grid)
    print(result)

if __name__ == "__main__":
    main()