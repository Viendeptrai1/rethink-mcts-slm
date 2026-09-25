import sys

def min_flats_to_turn_off(n, lights):
    # Initialize the count of disturbed flats
    disturbed_count = 0
    
    # Iterate through the flats to count disturbances
    for i in range(1, n - 1):
        if lights[i - 1] == 1 and lights[i] == 0 and lights[i + 1] == 1:
            disturbed_count += 1
    
    # To solve the problem, we need to turn off at least half of the disturbed flats
    # because each turned off flat can potentially resolve two disturbances.
    return (disturbed_count + 1) // 2

# Read input from standard input
input = sys.stdin.read
data = input().split()

# Parse the input
n = int(data[0])
lights = list(map(int, data[1:]))

# Calculate the result
result = min_flats_to_turn_off(n, lights)

# Print the result to standard output
print(result)