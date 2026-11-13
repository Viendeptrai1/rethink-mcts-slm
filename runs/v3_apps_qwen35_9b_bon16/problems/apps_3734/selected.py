import sys

def solve():
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    def get_index(name):
        return days.index(name)
    
    def next_month_days(month_idx):
        # Days in months for a non-leap year: 
        # Jan=31, Feb=28, Mar=31, Apr=30, May=31, Jun=30, Jul=31, Aug=31, Sep=30, Oct=31, Nov=30, Dec=31
        months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if 0 <= month_idx < 11:
            return months_days[month_idx] % 7
        return 0 # Should not be reached as we check up to 11
    
    try:
        input1 = sys.stdin.readline().strip()
        input2 = sys.stdin.readline().strip()
    except ValueError:
        return

    if not input1 or not input2:
        return

    d1_idx = get_index(input1)
    d2_idx = get_index(input2)

    # Check pairs of consecutive months (12 pairs in a year)
    possible = False
    for m in range(11):
        shift = next_month_days(m)
        if (d1_idx + shift) % 7 == d2_idx:
            possible = True
            break

    if possible:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()