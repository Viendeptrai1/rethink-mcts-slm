def find_earliest_not_so_rainy_day(n, x, y, rain_amounts):
    # Check each day if it is not so rainy
    for d in range(1, n + 1):
        is_not_so_rainy = True
        # Check the days before d
        for i in range(max(1, d - x), d):
            if rain_amounts[d - 1] >= rain_amounts[i - 1]:
                is_not_so_rainy = False
                break
        # If it's not so rainy, check the days after d
        if is_not_so_rainy:
            for i in range(d + 1, min(n + 1, d + y + 1)):
                if rain_amounts[d - 1] >= rain_amounts[i - 1]:
                    is_not_so_rainy = False
                    break
        # If the day is not so rainy, return its index
        if is_not_so_rainy:
            return d

    # The problem guarantees that an answer always exists, so we should never reach here.
    return -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input values
n = int(data[0])
x = int(data[1])
y = int(data[2])
rain_amounts = list(map(int, data[3:]))

# Call the function and print the result
result = find_earliest_not_so_rainy_day(n, x, y, rain_amounts)
print(result)