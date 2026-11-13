def min_spots(n, H):
    if n <= H:
        return 1
    elif n == H + 1:
        return 2
    else:
        remaining_sand = n - H - 1
        spots = 2
        while remaining_sand > 0:
            spots += 1
            remaining_sand -= spots - 1
        return spots

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
H = int(data[1])

print(min_spots(n, H))