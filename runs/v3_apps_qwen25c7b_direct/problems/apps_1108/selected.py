def count_rooms_for_george_and_alex(n, rooms):
    count = 0
    for p_i, q_i in rooms:
        if q_i - p_i >= 2:
            count += 1
    return count

# Example usage:
n = int(input())
rooms = [tuple(map(int, input().split())) for _ in range(n)]
print(count_rooms_for_george_and_alex(n, rooms))