import sys

def solve():
    days_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    input_data = sys.stdin.read().split()
    if len(input_data) < 2:
        return

    day1_name = input_data[0].strip()
    day2_name = input_data[1].strip()

    d1 = days_map[day1_name]
    d2 = days_map[day2_name]

    # Days in each month of a non-leap year
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    possible = False
    for i in range(11):
        shift = month_days[i] % 7
        if (d1 + shift) % 7 == d2:
            possible = True
            break

    if possible:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()