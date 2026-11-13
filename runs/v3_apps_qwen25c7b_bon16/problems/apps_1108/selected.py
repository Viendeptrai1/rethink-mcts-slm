def count_free_rooms(n, rooms):
    count = 0
    for room in rooms:
        if room[1] - room[0] >= 2:
            count += 1
    return count

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
rooms = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]

result = count_free_rooms(n, rooms)
print(result)