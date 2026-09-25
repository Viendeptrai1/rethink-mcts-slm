import sys

# Read the input integer
a = int(sys.stdin.read().strip())

# Calculate the number of 1s in the binary representation of a
result = bin(a).count('1')

# Print the result
print(result)