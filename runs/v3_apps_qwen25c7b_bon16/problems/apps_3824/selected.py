def min_path(x1, y1, x2, y2):
    # Calculate the Manhattan distance from the starting point to the flag
    distance_to_flag = abs(x1 - x2) + abs(y1 - y2)
    # The total path length is twice the distance to the flag plus 4 (to form a rectangle)
    total_path_length = 2 * distance_to_flag + 4
    return total_path_length

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    x1, y1 = int(data[0]), int(data[1])
    x2, y2 = int(data[2]), int(data[3])
    print(min_path(x1, y1, x2, y2))