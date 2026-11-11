def is_possible(first_day, second_day):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    first_day_index = days_of_week.index(first_day)
    second_day_index = days_of_week.index(second_day)
    
    for i in range(12):
        if (first_day_index + sum(month_lengths[:i])) % 7 == second_day_index:
            return "YES"
    
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Call the function and print the result
print(is_possible(data[0], data[1]))