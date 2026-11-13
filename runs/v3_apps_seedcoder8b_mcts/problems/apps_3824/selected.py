def minimal_quadcopter_path(x1, y1, x2, y2):
    # Calculate the Manhattan distance from the start to the flag
    distance_to_flag = abs(x1 - x2) + abs(y1 - y2)
    # The path needs to go around the flag, so we add 2 to the distance
    # One tick to go to the flag, one tick to stay inside the flag,
    # and one tick to return to the start.
    return distance_to_flag + 2

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    x1, y1 = int(data[0]), int(data[1])
    x2, y2 = int(data[2]), int(data[3])
    print(minimal_quadcopter_path(x1, y1, x2, y2))