def count_rooms_for_george_and_alex(n, rooms):
    count = 0
    for p, q in rooms:
        if q - p >= 2:
            count += 1
    return count

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    rooms = []
    index = 1
    for _ in range(n):
        p = int(data[index])
        q = int(data[index + 1])
        rooms.append((p, q))
        index += 2
    
    result = count_rooms_for_george_and_alex(n, rooms)
    print(result)