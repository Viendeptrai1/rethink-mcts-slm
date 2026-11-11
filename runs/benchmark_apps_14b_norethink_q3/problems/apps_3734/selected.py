def is_possible(first_day, second_day):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    first_index = days_of_week.index(first_day)
    second_index = days_of_week.index(second_day)
    
    # Calculate the difference in days between the two days
    difference = (second_index - first_index) % 7
    
    # Check if this difference is a possible number of days between the first day of two consecutive months
    for length in month_lengths:
        if length % 7 == difference:
            return "YES"
    
    return "NO"

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Call the function with the input data
result = is_possible(data[0], data[1])

# Print the result to stdout
print(result)