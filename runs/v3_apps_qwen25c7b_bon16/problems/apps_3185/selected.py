import math

def find_n_factorial(value):
    n = 0
    while math.factorial(n) < value:
        n += 1
    return n if math.factorial(n) == value else None

# Input reading
value = int(input().strip())
# Output the result
print(find_n_factorial(value))