import sys

# Read input from standard input
x = float(sys.stdin.read().strip())

# Convert the floating-point number to an integer by multiplying by 10^6
x_int = int(x * 10**6)

# Calculate the first integer by dividing by 50 and taking the result modulo 10
first_integer = (x_int // 50) % 10

# Ensure the first integer is between 1 and 10
if first_integer == 0:
    first_integer = 10

# Calculate the second integer by taking the remainder when divided by 10
second_integer = x_int % 10

# Ensure the second integer is between 1 and 10
if second_integer == 0:
    second_integer = 10

# Print the two integers separated by a space
print(first_integer, second_integer)