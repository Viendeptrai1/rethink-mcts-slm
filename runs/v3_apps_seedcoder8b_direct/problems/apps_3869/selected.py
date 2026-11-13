import math

def calculate_overlap_area(w, h, alpha):
    # Convert angle from degrees to radians
    alpha_rad = math.radians(alpha)
    
    # Calculate the new dimensions of the rotated rectangle
    w_prime = abs(w * math.cos(alpha_rad))
    h_prime = abs(h * math.sin(alpha_rad))
    
    # Calculate the area of the original rectangle
    area_original = w * h
    
    # Calculate the area of the rotated rectangle
    area_rotated = w_prime * h_prime
    
    # Calculate the overlap area
    overlap_area = min(w, w_prime) * min(h, h_prime)
    
    return overlap_area

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    w = int(data[0])
    h = int(data[1])
    alpha = int(data[2])
    
    result = calculate_overlap_area(w, h, alpha)
    print(f"{result:.9f}")

if __name__ == "__main__":
    main()