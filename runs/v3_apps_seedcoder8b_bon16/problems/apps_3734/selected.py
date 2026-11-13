def can_have_same_weekday(day1, day2):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day1_index = days_of_week.index(day1)
    day2_index = days_of_week.index(day2)
    
    if day1_index == day2_index:
        return True
    
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for i in range(12):
        if (day1_index + days_in_months[i]) % 7 == day2_index:
            return True
    return False

import sys
input = sys.stdin.read
data = input().strip().split()
day1 = data[0]
day2 = data[1]

if can_have_same_weekday(day1, day2):
    print("YES")
else:
    print("NO")