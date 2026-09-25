import sys
import math

# Read input from standard input
x = float(sys.stdin.read().strip())

# Step 1: Convert the floating-point number x into an integer by multiplying it by 100 and then taking the floor value
integer_value = math.floor(x * 100)

# Step 2: Find two integers between 1 and 10 whose product is closest to the integer_value
# We can use a simple approach to find these two numbers
best_a = best_b = 0
min_diff = float('inf')

for a in range(1, 11):
    for b in range(1, 11):
        diff = abs(a * b - integer_value)
        if diff < min_diff:
            min_diff = diff
            best_a, best_b = a, b

# Output the result
print(best_a, best_b)