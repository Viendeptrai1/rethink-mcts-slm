def count_days_with_free_food(N, events):
    # Initialize a set to keep track of unique days with free food
    free_food_days = set()
    
    # Iterate over each event
    for s_i, t_i in events:
        # Add all days from s_i to t_i (inclusive) to the set
        for day in range(s_i, t_i + 1):
            free_food_days.add(day)
    
    # The number of unique days with free food is the size of the set
    return len(free_food_days)

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Parse the number of events
N = int(data[0])

# Parse the events
events = []
index = 1
for _ in range(N):
    s_i = int(data[index])
    t_i = int(data[index + 1])
    events.append((s_i, t_i))
    index += 2

# Calculate and print the result
result = count_days_with_free_food(N, events)
print(result)