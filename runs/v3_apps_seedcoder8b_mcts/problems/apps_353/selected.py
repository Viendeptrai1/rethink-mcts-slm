def moon_phase_prediction(n, records):
    # Define the cycle of the moon's visible size
    cycle = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    # Determine the current phase in the cycle
    current_phase = records[-1]
    current_index = cycle.index(current_phase)
    
    # Determine the next day's phase
    next_phase = cycle[(current_index + 1) % len(cycle)]
    
    # Check the trend in the last few days
    if n < 2:
        return -1
    
    # Check if the last two days show a consistent trend
    if records[-1] > records[-2]:
        return "UP"
    elif records[-1] < records[-2]:
        return "DOWN"
    else:
        # If the last two days are the same, we can't determine the trend
        return -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
records = list(map(int, data[1:n+1]))

# Get the result and print it
result = moon_phase_prediction(n, records)
print(result)