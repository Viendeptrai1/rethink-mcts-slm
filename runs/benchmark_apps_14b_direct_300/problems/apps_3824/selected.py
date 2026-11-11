import sys

def min_quadcopter_path(x1, y1, x2, y2):
    # Calculate the Manhattan distance between the start and the flag
    dist_to_flag = abs(x1 - x2) + abs(y1 - y2)
    
    # The minimal path will be to go to the flag, then make a rectangle around it,
    # and return back to the start. The rectangle will have sides of length
    # (abs(x1 - x2) + 2) and (abs(y1 - y2) + 2).
    min_path_length = 2 * (dist_to_flag + 2)
    
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