def min_cost_to_paint(n, m, rectangles):
    # Find the minimum and maximum row and column indices of the black cells
    min_row = min(rec[1] for rec in rectangles)
    max_row = max(rec[3] for rec in rectangles)
    min_col = min(rec[0] for rec in rectangles)
    max_col = max(rec[2] for rec in rectangles)
    
    # Calculate the dimensions of the smallest rectangle that covers all black cells
    h = max_row - min_row + 1
    w = max_col - min_col + 1
    
    # Return the cost to paint this rectangle
    return min(h, w)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    rectangles = []
    index = 2
    for _ in range(m):
        x1 = int(data[index])
        y1 = int(data[index + 1])
        x2 = int(data[index + 2])
        y2 = int(data[index + 3])
        rectangles.append((x1, y1, x2, y2))
        index += 4
    
    result = min_cost_to_paint(n, m, rectangles)
    print(result)