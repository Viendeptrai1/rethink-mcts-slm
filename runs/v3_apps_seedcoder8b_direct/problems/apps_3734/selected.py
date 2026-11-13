def can_have_same_first_days(day1, day2):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day1_index = days_of_week.index(day1)
    day2_index = days_of_week.index(day2)
    
    # Check if the difference between the indices is a multiple of 7
    # This means they are the same day of the week
    if (day2_index - day1_index) % 7 == 0:
        return "YES"
    
    # Check if the difference is 6 days, which also means they are the same day of the week
    if abs(day2_index - day1_index) == 6:
        return "YES"
    
    return "NO"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    day1 = data[0]
    day2 = data[1]
    print(can_have_same_first_days(day1, day2))