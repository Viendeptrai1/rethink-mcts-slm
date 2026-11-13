import sys

def expected_max_dots(m, n):
    # Calculate the expected value for a single dice roll
    expected_value_single_roll = sum((i + 1) * (1 / m) for i in range(m))
    
    # Since the rolls are independent, the expected value for max over n rolls
    # is given by the expected value of a geometric distribution with success probability
    # equal to the expected value of a single roll minus 1 divided by the expected value of a single roll.
    p_success = expected_value_single_roll - 1
    expected_value_max = (expected_value_single_roll * p_success) / (1 - p_success)
    
    return expected_value_max

# Read input
input_line = sys.stdin.readline().strip()
m, n = map(int, input_line.split())

# Calculate and print the result
result = expected_max_dots(m, n)
print(f"{result:.10f}")