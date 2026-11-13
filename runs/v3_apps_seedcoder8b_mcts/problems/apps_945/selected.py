def semi_circles_intersect(x1, x2):
    # Calculate the radius of the semi-circle
    radius = abs(x2 - x1) / 2
    # Calculate the distance between the centers
    distance = abs(x2 - x1)
    # Check if the semi-circles intersect above the x-axis
    return distance < 2 * radius

def has_self_intersections(n, points):
    for i in range(n - 1):
        if semi_circles_intersect(points[i], points[i + 1]):
            return "yes"
    return "no"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    points = list(map(int, data[1:n+1]))
    
    result = has_self_intersections(n, points)
    print(result)

if __name__ == "__main__":
    main()