def min_distance_to_cow(n, k, rooms):
    # Convert the string of rooms into a list of indices where the room is free
    free_rooms = [i for i in range(n) if rooms[i] == '0']
    
    # Initialize the minimum distance to a large number
    min_distance = float('inf')
    
    # Iterate over each possible starting position for Farmer John's room
    for i in range(len(free_rooms) - k):
        # Calculate the distance to the nearest cow on either side
        left_distance = free_rooms[i + k] - free_rooms[i]
        right_distance = free_rooms[i + k + 1] - free_rooms[i + k]
        
        # Update the minimum distance found so far
        min_distance = min(min_distance, max(left_distance // 2, right_distance // 2))
    
    return min_distance

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    rooms = data[2]
    result = min_distance_to_cow(n, k, rooms)
    print(result)