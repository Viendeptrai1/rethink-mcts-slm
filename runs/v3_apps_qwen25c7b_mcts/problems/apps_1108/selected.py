def count_rooms_for_george_and_alex(n, rooms):
    count = 0
    for p_i, q_i in rooms:
        if q_i - p_i >= 2:
            count += 1
    return count

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
rooms = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]

result = count_rooms_for_george_and_alex(n, rooms)
print(result)