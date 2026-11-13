def check_days(day1, day2):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    index1 = days.index(day1)
    index2 = days.index(day2)
    
    # Calculate the difference in days between the two given days
    diff = (index2 - index1 + 7) % 7
    
    # Check if there exists a month where the first day is day1 and the second day is day2
    # This means the difference in days must be within the range of the shortest and longest month lengths
    return 1 <= diff <= 31

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Call the function and print the result
print("YES" if check_days(data[0], data[1]) else "NO")