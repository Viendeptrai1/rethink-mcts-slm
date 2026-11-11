import sys

def find_earliest_not_so_rainy_day(n, x, y, a):
    for d in range(n):
        is_not_so_rainy = True
        for j in range(max(0, d - x), d):
            if a[d] >= a[j]:
                is_not_so_rainy = False
                break
        for j in range(d + 1, min(n, d + y + 1)):
            if a[d] >= a[j]:
                is_not_so_rainy = False
                break
        if is_not_so_rainy:
            return d + 1
    return -1  # This line should never be reached because the problem guarantees a solution exists

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
x = int(data[1])
y = int(data[2])
a = list(map(int, data[3:]))

# Find and print the earliest not-so-rainy day
print(find_earliest_not_so_rainy_day(n, x, y, a))