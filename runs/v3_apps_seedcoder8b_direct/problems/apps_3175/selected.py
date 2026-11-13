import sys
import math

def max_sheep_pen_area(n, segments):
    # Sort the segments in non-decreasing order
    segments.sort()
    
    # Check if a valid polygon can be formed
    if n < 3 or segments[0] + segments[1] <= segments[-1]:
        return 0.0
    
    # Calculate the semi-perimeter
    s = sum(segments) / 2
    
    # Calculate the area using Heron's formula
    area = math.sqrt(s * (s - segments[0]) * (s - segments[1]) * (s - segments[2]))
    
    return area

def main():
    input_data = sys.stdin.read().strip()
    data = list(map(int, input_data.split()))
    
    n = data[0]
    segments = data[1:]
    
    result = max_sheep_pen_area(n, segments)
    print(f"{result:.3f}")

if __name__ == "__main__":
    main()