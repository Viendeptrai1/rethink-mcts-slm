def min_path(x1, y1, x2, y2):
    # Calculate the absolute differences in x and y coordinates
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    
    # The minimum path length is the sum of twice the differences plus 4 (to form a rectangle)
    return 2 * (dx + dy) + 4

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    x1, y1 = int(data[0]), int(data[1])
    x2, y2 = int(data[2]), int(data[3])
    print(min_path(x1, y1, x2, y2))