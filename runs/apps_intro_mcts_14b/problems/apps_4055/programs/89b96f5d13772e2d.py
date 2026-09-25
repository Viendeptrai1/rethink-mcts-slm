import sys

def min_lights_to_turn_off(n, lights):
    disturbances = []
    
    # Identify all disturbances
    for i in range(1, n - 1):
        if lights[i - 1] == 1 and lights[i] == 0 and lights[i + 1] == 1:
            disturbances.append(i)
    
    # If there are no disturbances, return 0
    if not disturbances:
        return 0
    
    # Calculate the minimum number of lights to turn off
    k = 0
    i = 0
    while i < len(disturbances):
        # Turn off the light in the current flat or one of its neighbors
        if i + 1 < len(disturbances) and disturbances[i + 1] == disturbances[i] + 2:
            # If the next disturbance is two flats away, we can turn off one light
            k += 1
            i += 2
        else:
            # Otherwise, we need to turn off two lights
            k += 2
            i += 1
    
    return k

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
lights = list(map(int, data[1:]))

# Find and print the result
result = min_lights_to_turn_off(n, lights)
print(result)