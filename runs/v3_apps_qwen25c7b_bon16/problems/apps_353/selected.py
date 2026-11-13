def moon_phase_prediction(n, moon_sizes):
    if n == 1:
        return -1
    
    current_size = moon_sizes[-1]
    previous_size = moon_sizes[-2]
    
    if current_size > previous_size:
        return "UP"
    elif current_size < previous_size:
        return "DOWN"
    else:
        return -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
moon_sizes = list(map(int, data[1:]))

result = moon_phase_prediction(n, moon_sizes)
print(result)