import sys
import math
from collections import deque

def calculate_explosions(R, C, layout):
    def euclidean_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Find all positions of 'X' (rude passengers) and 'L' (empty seats)
    passengers = []
    seats = []
    
    for r in range(R):
        for c in range(C):
            if layout[r][c] == 'X':
                passengers.append((r, c))
            elif layout[r][c] == 'L':
                seats.append((r, c))
    
    # If there are no seats, return 0 explosions
    if not seats:
        return 0
    
    # Function to simulate the movement of passengers
    def simulate_movement(passengers, seats):
        queue = deque(passengers)
        seated = set()
        explosions = 0
        
        while queue:
            r, c = queue.popleft()
            if (r, c) in seated:
                continue
            
            # Find the closest seat
            min_distance = float('inf')
            closest_seat = None
            
            for seat in seats:
                if seat not in seated:
                    distance = euclidean_distance(r, c, seat[0], seat[1])
                    if distance < min_distance:
                        min_distance = distance
                        closest_seat = seat
            
            if closest_seat:
                # Check if there's another passenger equally close to this seat
                equally_close = [p for p in queue if euclidean_distance(p[0], p[1], closest_seat[0], closest_seat[1]) == min_distance]
                
                if equally_close:
                    # All equally close, explode
                    explosions += 1
                    for passenger in equally_close:
                        queue.remove(passenger)
                    queue.append((r, c))  # Re-add current passenger to try again later
                else:
                    # Sit at the closest seat
                    seated.add(closest_seat)
            else:
                # No seats available, passenger will not move
                pass
        
        return explosions
    
    return simulate_movement(passengers, seats)

def main():
    input = sys.stdin.read
    data = input().split()
    R = int(data[0])
    C = int(data[1])
    layout = data[2:]
    
    result = calculate_explosions(R, C, layout)
    print(result)

if __name__ == "__main__":
    main()