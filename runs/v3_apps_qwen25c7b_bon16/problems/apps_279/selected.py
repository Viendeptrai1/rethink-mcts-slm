import sys
from typing import List

def max_path_length(v1: int, v2: int, t: int, d: int) -> int:
    # Calculate the minimum and maximum speeds over t seconds
    min_speed = max(v1 - d * (t - 1), v2 - d * (t - 1))
    max_speed = min(v1 + d * (t - 1), v2 + d * (t - 1))
    
    # Calculate the maximum possible length of the path section
    if min_speed > max_speed:
        return 0
    else:
        # Use the arithmetic series sum formula to calculate the maximum length
        return ((max_speed + min_speed) * t) // 2

# Read input from stdin
input_lines = sys.stdin.readlines()
v1, v2 = map(int, input_lines[0].split())
t, d = map(int, input_lines[1].split())

# Calculate and print the result
result = max_path_length(v1, v2, t, d)
print(result)