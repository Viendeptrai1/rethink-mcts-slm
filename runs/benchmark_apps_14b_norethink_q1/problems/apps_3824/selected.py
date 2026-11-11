import sys

def main():
    import sys
    x1, y1 = map(int, sys.stdin.readline().split())
    x2, y2 = map(int, sys.stdin.readline().split())
    
    # Calculate the Manhattan distance
    manhattan_distance = abs(x1 - x2) + abs(y1 - y2)
    
    # The minimal path length is twice the Manhattan distance plus 4
    # because we need to make a rectangle around the flag
    minimal_path_length = 2 * manhattan_distance + 4
    
    print(minimal_path_length)

if __name__ == "__main__":
    main()