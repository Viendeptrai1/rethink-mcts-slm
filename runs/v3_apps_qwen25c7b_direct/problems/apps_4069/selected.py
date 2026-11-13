import sys

def min_absolute_value(X, K, D):
    # Calculate the remainder when K is divided by 2
    remainder = K % 2
    
    # If K is even, Takahashi can always end up at coordinate X
    if remainder == 0:
        return abs(X)
    
    # If K is odd, Takahashi can minimize the absolute value by moving towards X
    else:
        # Move towards X with one step and then stay still
        return abs(X - D)

# Read input from standard input
input = sys.stdin.read
data = input().split()

# Parse the input values
X = int(data[0])
K = int(data[1])
D = int(data[2])

# Call the function and print the result
print(min_absolute_value(X, K, D))