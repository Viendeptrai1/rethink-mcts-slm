def earliest_not_so_rainy_day(n, x, y, a):
    for i in range(n):
        is_not_so_rainy = True
        for j in range(max(0, i - x), i):
            if a[i] >= a[j]:
                is_not_so_rainy = False
                break
        for j in range(i + 1, min(n, i + y + 1)):
            if a[i] >= a[j]:
                is_not_so_rainy = False
                break
        if is_not_so_rainy:
            return i + 1
    return -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
x = int(data[1])
y = int(data[2])
a = list(map(int, data[3:]))

print(earliest_not_so_rainy_day(n, x, y, a))