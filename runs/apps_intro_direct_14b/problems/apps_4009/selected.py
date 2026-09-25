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
    # This is the minimum number of operations needed
    operations = bin(difference).count('1')
    
    return operations

# Read input from standard input
input = sys.stdin.read
data = input().split()

n = int(data[0])
x = int(data[1])
y = int(data[2])
number = data[3]

# Calculate and print the result
result = min_operations(n, x, y, number)
print(result)