def count_free_food_days(N, events):
    # Create a set to store unique days with free food
    free_food_days = set()
    
    # Iterate through each event
    for s_i, t_i in events:
        # Add each day of the event to the set
        for day in range(s_i, t_i + 1):
            free_food_days.add(day)
    
    # Return the number of unique days with free food
    return len(free_food_days)

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
N = int(data[0])
events = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

# Calculate and print the result
print(count_free_food_days(N, events))