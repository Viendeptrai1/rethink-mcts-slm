def max_continuous_rest_hours(n, schedule):
    # Concatenate the schedule with itself to handle the circular nature
    extended_schedule = schedule + schedule
    
    # Initialize variables to track the maximum rest hours and current rest hours
    max_rest_hours = 0
    current_rest_hours = 0
    
    # Iterate over the extended schedule
    for i in range(2 * n):
        if extended_schedule[i] == 1:
            current_rest_hours += 1
        else:
            current_rest_hours = 0
        
        # Update the maximum rest hours if the current rest hours exceed it
        if i >= n:
            max_rest_hours = max(max_rest_hours, current_rest_hours)
    
    return max_rest_hours

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
schedule = list(map(int, data[1:n+1]))

# Output the result
print(max_continuous_rest_hours(n, schedule))