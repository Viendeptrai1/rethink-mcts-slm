def moon_phase_prediction(n, records):
    # Define the cycle of the moon's visible size
    cycle = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    # Determine the expected next day's size based on the current cycle
    next_day_size = cycle[(records[-1] + 1) % 30]
    
    # Check the trend in the last 3 days
    if n >= 3:
        if records[-3] < records[-2] < records[-1]:
            return "UP"
        elif records[-3] > records[-2] > records[-1]:
            return "DOWN"
    
    # If there's not enough data to determine the trend, return -1
    return -1

# Read input
n = int(input().strip())
records = list(map(int, input().strip().split()))

# Get the result and print it
result = moon_phase_prediction(n, records)
print(result)