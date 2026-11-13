def can_have_same_first_days(day1, day2):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day1_index = days_of_week.index(day1)
    day2_index = days_of_week.index(day2)
    
    # Check if the difference between the two days is 31 days
    return (day2_index - day1_index) % 7 == 31 % 7

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    day1 = data[0]
    day2 = data[1]
    if can_have_same_first_days(day1, day2):
        print("YES")
    else:
        print("NO")