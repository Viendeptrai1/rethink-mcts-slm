import sys

def main():
    import sys
    
    def read_ints():
        return map(int, sys.stdin.read().split())
    
    x1, y1, x2, y2 = read_ints()
    
    # Calculate the Manhattan distance between the starting point and the flag
    manhattan_distance = abs(x1 - x2) + abs(y1 - y2)
    
    # The minimal path length is twice the Manhattan distance plus 4
    minimal_path_length = 2 * manhattan_distance + 4
    
    print(minimal_path_length)

if __name__ == "__main__":
    main()