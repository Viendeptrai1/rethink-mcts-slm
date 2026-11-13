def min_coupons(N, trips):
    coupons = 0
    current_zone = 0
    current_time = 0

    for zone, time in trips:
        # Calculate the cost of a new ticket for this trip
        cost = 2 + abs(current_zone - zone)
        coupons += cost

        # Update current zone and time
        current_zone = zone
        current_time = time

    return coupons

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    trips = []
    index = 1
    for _ in range(N):
        Z = int(data[index])
        T = int(data[index + 1])
        trips.append((Z, T))
        index += 2
    
    result = min_coupons(N, trips)
    print(result)

if __name__ == "__main__":
    main()