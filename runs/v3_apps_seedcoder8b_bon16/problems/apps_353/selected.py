def moon_phase_prediction(n, records):
    # Moon cycle period
    cycle_length = 30
    # Moon cycle pattern
    moon_cycle = list(range(16)) + list(range(14, 0, -1))

    # Determine the phase of the last day in the input
    last_day_phase = records[-1]

    # Determine what the phase would be on the next day
    next_day_phase = moon_cycle[(records.index(last_day_phase) + 1) % cycle_length]

    # Check if the trend is clear
    if n > 1:
        # Check the trend of the last two days
        if records[-2] < records[-1]:
            return "UP"
        elif records[-2] > records[-1]:
            return "DOWN"
        else:
            # If the last two days are equal, we can't determine the trend
            return -1
    
    # If there is only one day of data, we cannot determine the next trend
    return -1

# Reading input
import sys
input = sys.stdin.read
data = input().strip().split()
n = int(data[0])
records = list(map(int, data[1:]))

# Calculating and printing the result
result = moon_phase_prediction(n, records)
print(result)