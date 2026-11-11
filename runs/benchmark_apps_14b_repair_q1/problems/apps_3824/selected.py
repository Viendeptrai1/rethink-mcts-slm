import sys

def min_quadcopter_path(x1, y1, x2, y2):
    # Calculate the Manhattan distance between the start and flag points
    dist_start_to_flag = abs(x2 - x1) + abs(y2 - y1)
    
    # The minimal path will be a rectangle that surrounds the flag point
    # with the start and finish points at opposite corners of the rectangle
    # The extra 4 steps account for going around the flag point
    min_path_length = 2 * (dist_start_to_flag + 2)
    
    return min_path_length

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    x1 = int(data[0])
    y1 = int(data[1])
    x2 = int(data[2])
    y2 = int(data[3])
    
    result = min_quadcopter_path(x1, y1, x2, y2)
    print(result)

if __name__ == "__main__":
    main()