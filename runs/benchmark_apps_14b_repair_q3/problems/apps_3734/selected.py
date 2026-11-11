def is_possible(first_day, second_day):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    first_day_index = days_of_week.index(first_day)
    second_day_index = days_of_week.index(second_day)
    
    # Check if the difference between the days modulo 7 matches any month length minus one
    for length in month_lengths:
        if (second_day_index - first_day_index) % 7 == (length - 1) or (first_day_index == second_day_index):
            return "YES"
    
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Call the function and print the result
print(is_possible(data[0], data[1]))