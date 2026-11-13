import sys

def calculate_probability(Tg, Ty, Tr, observations, query_time, query_color):
    total_cycle = Tg + Ty + Tr
    current_time = 0
    current_color = 'red'
    
    # Determine the starting time T based on the first observation
    for time, color in observations:
        if color == 'green':
            current_time = time - Tg
            break
    
    # Calculate the effective time within the cycle
    effective_time = (query_time - current_time) % total_cycle
    
    # Determine the color at the query time
    if effective_time < Tg:
        query_color_at_time = 'green'
    elif effective_time < Tg + Ty:
        query_color_at_time = 'yellow'
    else:
        query_color_at_time = 'red'
    
    # Calculate the probability
    if query_color_at_time == query_color:
        return 1.0 / 3.0
    else:
        return 0.0

# Read input
input = sys.stdin.read
data = input().split()

Tg = int(data[0])
Ty = int(data[1])
Tr = int(data[2])

n = int(data[3 * 2 + 1])

observations = []
for i in range(n):
    time = int(data[3 * i + 3])
    color = data[3 * i + 4]
    observations.append((time, color))

query_time = int(data[3 * n + 3])
query_color = data[3 * n + 4]

# Calculate and print the result
result = calculate_probability(Tg, Ty, Tr, observations, query_time, query_color)
print(f"{result:.3f}")