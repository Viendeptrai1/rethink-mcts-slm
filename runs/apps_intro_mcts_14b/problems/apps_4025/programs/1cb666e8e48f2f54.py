import sys

def max_days(a, b, c):
    # Calculate the maximum number of days the cat can eat without additional food purchases
    # by simulating the consumption of food starting from each day of the week.
    
    # Days of the week and their corresponding food consumption pattern
    days = [
        (3, 2, 2),  # Starting from Monday
        (2, 2, 3),  # Starting from Tuesday
        (2, 3, 2),  # Starting from Wednesday
        (3, 2, 2),  # Starting from Thursday
        (2, 2, 3),  # Starting from Friday
        (2, 3, 2),  # Starting from Saturday
        (3, 2, 2)   # Starting from Sunday
    ]
    
    max_days = 0
    
    for fish, rabbit, chicken in days:
        days_count = 0
        while a >= fish and b >= rabbit and c >= chicken:
            a -= fish
            b -= rabbit
            c -= chicken
            days_count += 1
        max_days = max(max_days, days_count)
    
    return max_days

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])
c = int(data[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)