import sys
from collections import deque

def calculate_distance(r, c, x, y):
    return ((r - x) ** 2 + (c - y) ** 2) ** 0.5

def find_closest_seats(R, C, tram):
    seats = []
    passengers = []
    
    for r in range(R):
        for c in range(C):
            if tram[r][c] == 'L':
                seats.append((r, c))
            elif tram[r][c] == 'X':
                passengers.append((r, c))
    
    explosions = 0
    
    while passengers:
        min_distance = float('inf')
        closest_seat = None
        closest_passengers = []
        
        for seat in seats:
            distances = [calculate_distance(seat[0], seat[1], passenger[0], passenger[1]) for passenger in passengers]
            min_dist = min(distances)
            
            if min_dist < min_distance:
                min_distance = min_dist
                closest_seat = seat
                closest_passengers = [passengers[i] for i, d in enumerate(distances) if d == min_dist]
            elif min_dist == min_distance:
                closest_passengers.extend([passengers[i] for i, d in enumerate(distances) if d == min_dist])
        
        if len(closest_passengers) > 1:
            explosions += 1
        
        seats.remove(closest_seat)
        for passenger in closest_passengers:
            passengers.remove(passenger)
    
    return explosions

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    R = int(data[0])
    C = int(data[1])
    
    tram = []
    index = 2
    for _ in range(R):
        row = data[index]
        tram.append(row)
        index += 1
    
    result = find_closest_seats(R, C, tram)
    print(result)

if __name__ == "__main__":
    main()