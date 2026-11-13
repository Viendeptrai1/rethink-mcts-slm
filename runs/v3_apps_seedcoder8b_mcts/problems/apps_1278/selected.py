def find_earliest_not_so_rainy_day(n, x, y, rain_amounts):
    for d in range(1, n + 1):
        is_not_so_rainy = True
        # Check x days before day d
        for j in range(max(1, d - x), d):
            if rain_amounts[d - 1] >= rain_amounts[j - 1]:
                is_not_so_rainy = False
                break
        # Check y days after day d
        for j in range(d + 1, min(n + 1, d + y + 1)):
            if rain_amounts[d - 1] >= rain_amounts[j - 1]:
                is_not_so_rainy = False
                break
        if is_not_so_rainy:
            return d

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
x = int(data[1])
y = int(data[2])
rain_amounts = list(map(int, data[3:]))

# Find and print the earliest not so rainy day
print(find_earliest_not_so_rainy_day(n, x, y, rain_amounts))