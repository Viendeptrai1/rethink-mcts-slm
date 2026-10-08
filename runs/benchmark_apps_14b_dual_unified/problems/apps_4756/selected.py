import sys
import math

def calculate_a(N, points):
    total_x = 0
    total_y = 0
    total_xy = 0
    total_x2 = 0
    total_y2 = 0
    
    for x, y in points:
        total_x += x
        total_y += y
        total_xy += x * y
        total_x2 += x * x
        total_y2 += y * y
    
    # Calculate the optimal 'a' using the formula derived from minimizing the sum of squared distances
    numerator = total_y - total_x
    denominator = N
    
    return numerator / denominator

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = []
    
    index = 1
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        points.append((x, y))
        index += 2
    
    a = calculate_a(N, points)
    print(f"{a:.6f}")

if __name__ == "__main__":
    main()