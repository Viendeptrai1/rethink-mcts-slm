import sys

def expected_max(m, n):
    # Calculate the expected value for a single roll
    expected_single_roll = sum((i * (i + 1)) / 2 for i in range(1, m + 1)) / m
    
    # The expected maximum after n rolls is approximately n times the expected value of a single roll
    expected_max_value = n * expected_single_roll
    
    return expected_max_value

# Read input
input_line = sys.stdin.readline().strip()
m, n = map(int, input_line.split())

# Calculate and print the result
result = expected_max(m, n)
print(f"{result:.10f}")