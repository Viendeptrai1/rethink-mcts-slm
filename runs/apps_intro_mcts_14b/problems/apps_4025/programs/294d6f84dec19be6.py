import sys

def max_days(a, b, c):
    # Calculate the number of complete weeks the cat can survive
    # based on the least restrictive food type
    min_food = min(a // 3, b // 2, c)
    
    # Calculate the remaining food after these complete weeks
    remaining_a = a - min_food * 3
    remaining_b = b - min_food * 2
    remaining_c = c - min_food
    
    # Calculate the maximum number of additional days the cat can survive
    # with the remaining food
    additional_days = min(remaining_a, remaining_b, remaining_c)
    
    # Total days the cat can survive
    total_days = min_food * 7 + additional_days
    
    return total_days

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])
c = int(data[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)