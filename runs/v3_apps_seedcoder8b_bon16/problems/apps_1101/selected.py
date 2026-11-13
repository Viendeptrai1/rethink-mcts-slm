def minimum_distance_to_cows(n, k, rooms):
    # Find the positions of all free rooms
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # Function to check if it's possible to book k+1 rooms with max distance `max_dist`
    def can_place(max_dist):
        count = 0
        last_position = -1
        for room in free_rooms:
            if last_position == -1 or room - last_position > max_dist:
                count += 1
                last_position = room
            if count > k:
                return False
        return True

    # Binary search to find the minimum possible maximum distance
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if can_place(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    k = int(data[1])
    rooms = data[2]
    result = minimum_distance_to_cows(n, k, rooms)
    print(result)