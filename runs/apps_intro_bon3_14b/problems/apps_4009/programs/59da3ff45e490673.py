import sys

def min_operations(n, x, y, number):
    # The target remainder is 10^y
    target_remainder = 10**y
    
    # Convert the number to a list of integers for easier manipulation
    number = [int(digit) for digit in number]
    
    # Calculate the current remainder of the number modulo 10^x
    current_remainder = int(''.join(map(str, number[-x:])), 2)
    
    # Calculate the difference between the target and current remainders
    difference = (target_remainder - current_remainder) % (10**x)
    
    # Count the number of 1s in the binary representation of the difference
    # These are the positions where we need to flip bits to achieve the target remainder
    flips_needed = bin(difference).count('1')
    
    return flips_needed

# Read input from standard input
input = sys.stdin.read().split()
n = int(input[0])
x = int(input[1])
y = int(input[2])
number = input[3]

# Calculate and print the result
result = min_operations(n, x, y, number)
print(result)