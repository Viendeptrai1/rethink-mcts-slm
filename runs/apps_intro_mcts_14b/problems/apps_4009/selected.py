import sys

def min_operations(n, x, y, number):
    # Convert the number to a list of integers for easier manipulation
    number = [int(digit) for digit in number]
    
    # The target remainder is 10^y
    target_remainder = [0] * y + [1] + [0] * (x - y - 1)
    
    # Calculate the difference between the current last x digits and the target remainder
    operations = 0
    for i in range(x):
        if number[-x + i] != target_remainder[i]:
            operations += 1
    
    return operations

# Read input from standard input
input = sys.stdin.read().split()
n = int(input[0])
x = int(input[1])
y = int(input[2])
number = input[3]

# Calculate and print the result
result = min_operations(n, x, y, number)
print(result)