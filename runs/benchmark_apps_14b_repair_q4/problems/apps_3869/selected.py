import math

def intersecting_area(w, h, alpha):
    # Convert angle from degrees to radians
    alpha_rad = math.radians(alpha)
    
    # Calculate the half-widths and half-heights
    hw1, hh1 = w / 2, h / 2
    hw2, hh2 = hh1 * abs(math.cos(alpha_rad)), hw1 * abs(math.sin(alpha_rad))
    
    # Calculate the intersection area
    if alpha == 0 or alpha == 180:
        return min(w, hw2) * min(h, hh2)
    elif alpha == 90 or alpha == 270:
        return min(w, hh2) * min(h, hw2)
    else:
        # General case
        x_overlap = min(hw1 + hh2 * abs(math.sin(alpha_rad)), hw2 + hh1 * abs(math.sin(alpha_rad)))
        y_overlap = min(hh1 + hw2 * abs(math.cos(alpha_rad)), hh2 + hw1 * abs(math.cos(alpha_rad)))
        return x_overlap * y_overlap

# Read input
w, h, alpha = map(int, input().split())

# Calculate and print the result
print(intersecting_area(w, h, alpha))