def count_free_food_days(N, events):
    # Initialize an array of size 365 with False values
    days_with_food = [False] * 365
    
    # Iterate through each event
    for s_i, t_i in events:
        # Mark the days from s_i to t_i (inclusive) as True
        for day in range(s_i - 1, t_i):
            days_with_food[day] = True
    
    # Count the number of days with free food
    return sum(days_with_food)

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Parse the input
N = int(data[0])
events = []
index = 1
for _ in range(N):
    s_i = int(data[index])
    t_i = int(data[index + 1])
    events.append((s_i, t_i))
    index += 2

# Calculate and print the result
result = count_free_food_days(N, events)
print(result)