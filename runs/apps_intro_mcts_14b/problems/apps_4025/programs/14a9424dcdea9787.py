import sys

def max_days(a, b, c):
    # Calculate the maximum number of days the cat can eat without additional food purchases
    # by considering the optimal starting day of the week.
    
    # Calculate the number of days the cat can eat with each type of food as the limiting factor
    days_with_fish = (a // 3) * 3 + min(a % 3, 3)
    days_with_rabbit = (b // 2) * 2 + min(b % 2, 2)
    days_with_chicken = c
    
    # The maximum number of days the cat can eat is the minimum of these values
    return max(days_with_fish, days_with_rabbit, days_with_chicken)

# Read input from standard input
input = sys.stdin.read
data = input().split()

# Parse the input values
a = int(data[0])
b = int(data[1])
c = int(data[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)