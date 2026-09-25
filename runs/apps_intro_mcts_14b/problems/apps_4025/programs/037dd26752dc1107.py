import sys

def max_days(a, b, c):
    # Calculate the maximum number of days for each starting day
    days_starting_monday = min(a // 3, b // 2, c)
    days_starting_tuesday = min(a // 3, b // 2, c // 2)
    days_starting_wednesday = min(a // 3, b, c // 2)
    days_starting_thursday = min(a // 3, b // 2, c)
    days_starting_friday = min(a // 3, b, c // 2)
    days_starting_saturday = min(a // 3, b // 2, c // 2)
    days_starting_sunday = min(a // 3, b // 2, c)
    
    # Return the maximum number of days among all starting days
    return max(days_starting_monday, days_starting_tuesday, days_starting_wednesday,
               days_starting_thursday, days_starting_friday, days_starting_saturday,
               days_starting_sunday)

# Read input
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])
c = int(data[2])

# Calculate and print the result
result = max_days(a, b, c)
print(result)