import sys

def min_operations(n, x, y, number):
    # The target remainder is 10^y
    target_remainder = 10**y
    
    # Calculate the prefix of the number that we need to match the target remainder
    target_prefix = str(target_remainder).zfill(x)
    
    # Initialize the count of operations
    operations = 0
    
    # Iterate over the last x digits of the number
    for i in range(n - x, n):
        if number[i] != target_prefix[i - (n - x)]:
            operations += 1
    
    return operations

# Read input
input = sys.stdin.read().split()
n = int(input[0])
x = int(input[1])
y = int(input[2])
number = input[3]

# Calculate and print the result
result = min_operations(n, x, y, number)
print(result)