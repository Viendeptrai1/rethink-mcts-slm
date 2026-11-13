import sys

def calculate_hours_in_world_a(T, X):
    return T / X

# Read input from standard input
input_line = sys.stdin.readline().strip()
T, X = map(int, input_line.split())

# Calculate the result
result = calculate_hours_in_world_a(T, X)

# Print the result
print(result)