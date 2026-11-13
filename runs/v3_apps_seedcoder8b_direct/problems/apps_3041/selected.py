def min_coupons(N, trips):
    # Initialize the current zone and time
    current_zone = 0
    current_time = 0
    total_coupons = 0

    for trip in trips:
        next_zone, next_time = trip

        # If the next trip is within 10000 seconds of the current time, check if it's in the same zone
        if next_time - current_time <= 10000:
            if current_zone != next_zone:
                # Calculate the cost of a new ticket
                total_coupons += 2 + abs(current_zone - next_zone)
                # Update the current zone
                current_zone = next_zone
        else:
            # If the next trip is more than 10000 seconds away, buy a new ticket
            total_coupons += 2 + abs(current_zone - next_zone)
            # Update the current zone and time
            current_zone = next_zone
            current_time = next_time

    return total_coupons

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
N = int(data[0])
trips = [(int(data[i]), int(data[i+1])) for i in range(1, 2*N, 2)]

# Get the result
result = min_coupons(N, trips)

# Print the result
print(result)