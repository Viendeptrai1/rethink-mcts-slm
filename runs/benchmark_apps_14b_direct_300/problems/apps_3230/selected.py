import sys
import math

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def find_closest_seats(tram, passengers):
    explosions = 0
    while passengers:
        min_distance = float('inf')
        closest_passenger = None
        closest_seat = None
        for px, py in passengers:
            for sx, sy in seats:
                distance = calculate_distance(px, py, sx, sy)
                if distance < min_distance:
                    min_distance = distance
                    closest_passenger = (px, py)
                    closest_seat = (sx, sy)
                elif distance == min_distance:
                    explosions += 1
                    passengers.remove(closest_passenger)
                    break
            else:
                continue
            break
        if closest_passenger:
            passengers.remove(closest_passenger)
            seats.remove(closest_seat)
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
    
    passengers = []
    seats = []
    
    for i in range(R):
        for j in range(C):
            if tram[i][j] == 'X':
                passengers.append((i, j))
            elif tram[i][j] == 'L':
                seats.append((i, j))
    
    result = find_closest_seats(tram, passengers)
    print(result)

if __name__ == "__main__":
    main()