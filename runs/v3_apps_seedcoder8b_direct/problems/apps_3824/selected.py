def minimal_quadcopter_path(x1, y1, x2, y2):
    # Calculate the Manhattan distance from the start to the flag
    distance_to_flag = abs(x1 - x2) + abs(y1 - y2)
    
    # Calculate the Manhattan distance from the flag to the start
    distance_back_to_start = abs(x2 - x1) + abs(y2 - y1)
    
    # The minimal path is twice the distance to the flag plus the distance back to the start
    # This accounts for the path going around the flag and returning to the start
    minimal_path_length = 2 * distance_to_flag + distance_back_to_start
    
    return minimal_path_length

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    x1, y1 = int(data[0]), int(data[1])
    x2, y2 = int(data[2]), int(data[3])
    print(minimal_quadcopter_path(x1, y1, x2, y2))