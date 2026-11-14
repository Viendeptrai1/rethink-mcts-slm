import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return
    
    points = []
    for _ in range(n):
        x = int(next(iterator))
        y = int(next(iterator))
        points.append((x, y))
    
    # Store points in sets for O(1) average time complexity lookups
    # x_to_points: maps x-coordinate to a set of y-coordinates at that x
    # y_to_points: maps y-coordinate to a set of x-coordinates at that y
    x_to_points = {}
    y_to_points = {}
    
    for x, y in points:
        if x not in x_to_points:
            x_to_points[x] = set()
        if y not in y_to_points:
            y_to_points[y] = set()
        x_to_points[x].add(y)
        y_to_points[y].add(x)
    
    count = 0
    
    # Iterate through each point considering it as the right-angle vertex
    for x, y in points:
        # Count points sharing the same x-coordinate (vertical leg candidates)
        # Exclude the point itself
        vertical_count = len(x_to_points[x]) - 1
        
        # Count points sharing the same y-coordinate (horizontal leg candidates)
        # Exclude the point itself
        horizontal_count = len(y_to_points[y]) - 1
        
        # If there are points in both directions, we can form triangles
        if vertical_count > 0 and horizontal_count > 0:
            count += vertical_count * horizontal_count
    
    print(count)

if __name__ == "__main__":
    solve()