import math

def calculate_intersected_area(w, h, alpha):
    # Convert angle from degrees to radians
    alpha_rad = math.radians(alpha)
    
    # Calculate half-widths and heights
    w_half = w / 2
    h_half = h / 2
    
    # Calculate the intersections using trigonometry
    x1 = abs(w_half * math.cos(alpha_rad)) + abs(h_half * math.sin(alpha_rad))
    x2 = abs(w_half * math.cos(alpha_rad)) - abs(h_half * math.sin(alpha_rad))
    y1 = abs(h_half * math.cos(alpha_rad)) + abs(w_half * math.sin(alpha_rad))
    y2 = abs(h_half * math.cos(alpha_rad)) - abs(w_half * math.sin(alpha_rad))
    
    # Calculate the area of intersection
    intersected_area = max(0, min(x1, x2) - max(-x1, -x2)) * max(0, min(y1, y2) - max(-y1, -y2))
    
    return intersected_area

# Main code to read input and output result
if __name__ == "__main__":
    w, h, alpha = map(int, input().split())
    result = calculate_intersected_area(w, h, alpha)
    print(result)