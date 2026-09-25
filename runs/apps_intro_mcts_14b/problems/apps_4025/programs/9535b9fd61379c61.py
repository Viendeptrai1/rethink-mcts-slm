import sys

def max_days(a, b, c):
    # Calculate the maximum number of days the cat can eat without additional food purchases
    # by considering the distribution of food types over the week.
    
    # Calculate the number of complete weeks the cat can survive
    # based on the least restrictive food type.
    max_weeks = min(a // 3, b // 2, c)
    
    # Calculate the remaining food after these complete weeks
    remaining_a = a - max_weeks * 3
    remaining_b = b - max_weeks * 2
    remaining_c = c - max_weeks
    
    # Calculate the maximum number of additional days the cat can eat
    # with the remaining food supplies.
    additional_days = 0
    if remaining_a > 0:
        additional_days += 1
    if remaining_b > 0:
        additional_days += 1
    if remaining_c > 0:
        additional_days += 1
    
    # Total days the cat can eat
    total_days = max_weeks * 7 + additional_days
    
    return total_days

# Read input from standard input
input = sys.stdin.read().split()
a = int(input[0])
b = int(input[1])
c = int(input[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)