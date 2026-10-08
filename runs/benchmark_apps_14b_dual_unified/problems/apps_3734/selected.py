def is_possible(first_day, second_day):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    first_index = days_of_week.index(first_day)
    second_index = days_of_week.index(second_day)
    
    day_difference = (second_index - first_index) % 7
    
    for length in month_lengths:
        if day_difference == length % 7:
            return "YES"
    
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()

first_day = data[0]
second_day = data[1]

# Output result
print(is_possible(first_day, second_day))