def check_days(day1, day2):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    index1 = days.index(day1)
    index2 = days.index(day2)
    
    # Calculate the difference in days between the two given days
    diff = (index2 - index1 + 7) % 7
    
    # Check if the difference is 1 or 6 (since 1 month has at least 28 days)
    return "YES" if diff == 1 or diff == 6 else "NO"

# Example usage:
# day1 = input().strip()
# day2 = input().strip()
# result = check_days(day1, day2)
# print(result)