import sys

def min_coupons(N, trips):
    current_ticket = None
    total_coupons = 0

    for Z, T in trips:
        if current_ticket is None or T >= current_ticket[1] or Z < current_ticket[0] or Z > current_ticket[2]:
            # Calculate the cost of a new ticket
            cost = 2 + abs(0 - Z)
            total_coupons += cost
            # Set the new ticket's validity
            current_ticket = (0, T, Z, T + 10000)
        else:
            # Update the ticket's end time if necessary
            current_ticket = (current_ticket[0], max(current_ticket[1], T), current_ticket[2], current_ticket[3])

    return total_coupons

if __name__ == "__main__":
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