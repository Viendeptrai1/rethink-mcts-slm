import math

def intersection_area(w, h, alpha):
    # Convert angle from degrees to radians
    alpha_rad = math.radians(alpha)
    
    # Calculate half-diagonals of the original and rotated rectangles
    d1 = math.sqrt((w / 2) ** 2 + (h / 2) ** 2)
    d2 = d1
    
    # Calculate the distance between the centers of the two rectangles
    d = abs(d1 * math.cos(alpha_rad))
    
    # Calculate the area of intersection
    if d <= w / 2:
        area = (w * h) / 2 * (1 - math.cos(math.asin(d / (w / 2))))
    else:
        area = (w * h) / 2 * (math.sin(math.pi / 2 - alpha_rad) + math.sin(math.pi / 2 - alpha_rad))
    
    return area

# Example usage
if __name__ == "__main__":
    w, h, alpha = map(int, input().split())
    result = intersection_area(w, h, alpha)
    print(result)