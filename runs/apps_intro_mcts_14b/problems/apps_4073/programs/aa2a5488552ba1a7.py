import sys

# Read input from standard input
input = sys.stdin.read
data = input().split()

# Parse the number of elements
n = int(data[0])

# Parse the list of integers
a = list(map(int, data[1:]))

# Calculate the sum of the integers
total_sum = sum(a)

# Find the remainder when the sum is divided by 10
result = total_sum % 10

# Print the result to standard output
print(result)