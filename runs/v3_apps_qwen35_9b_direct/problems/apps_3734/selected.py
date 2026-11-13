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

    try:
        line1 = sys.stdin.readline().strip()
        line2 = sys.stdin.readline().strip()
    except ValueError:
        return

    if not line1 or not line2:
        return

    d1 = days_map[line1]
    d2 = days_map[line2]

    months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(11):
        shift = months_days[i] % 7
        if (d1 + shift) % 7 == d2:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()