import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    a = int(input_data[0])
    b = int(input_data[1])
    c = int(input_data[2])
    d = int(input_data[3])
    
    # Sort the initial positions
    x = sorted([a, b, c])
    
    # We need to find a target position y such that the ropewalkers end up at:
    # y, y + d, y + 2d
    # The cost is |x[0] - y| + |x[1] - (y + d)| + |x[2] - (y + 2d)|
    # This can be rewritten as:
    # |x[0] - y| + |(x[1] - d) - y| + |(x[2] - 2d) - y|
    # This is a classic problem of finding a point y that minimizes the sum of absolute differences
    # to a set of points. The optimal y is the median of the transformed points.
    
    transformed = [x[0], x[1] - d, x[2] - 2*d]
    transformed.sort()
    
    # The median of 3 elements is the middle one
    y = transformed[1]
    
    # Calculate the total distance
    ans = abs(x[0] - y) + abs(x[1] - (y + d)) + abs(x[2] - (y + 2*d))
    
    print(ans)

if __name__ == "__main__":
    solve()