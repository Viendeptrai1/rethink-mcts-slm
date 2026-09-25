import sys

def find_integers(x):
    # Convert the float to an integer by multiplying by 100
    target = int(x * 100)
    
    # Start with the integer part of x as one of the numbers
    num1 = int(x)
    
    # Calculate the remaining value to be distributed
    remaining = target - (num1 * 10)
    
    # Determine the second number
    num2 = remaining // 10 + 1
    
    # Ensure both numbers are within the range 1 to 10
    if num1 > 10:
        num1 = 10
    if num2 > 10:
        num2 = 10
    
    return num1, num2

# Read input from standard input
x = float(sys.stdin.read().strip())

# Find the two integers
result = find_integers(x)

# Print the result
print(result[0], result[1])