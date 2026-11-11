import sys
import math

def calculate_a(N, points):
    sum_x = sum_y = sum_xy = sum_x2 = 0
    for x, y in points:
        sum_x += x
        sum_y += y
        sum_xy += x * y
        sum_x2 += x * x
    
    # Calculate the optimal 'a' using the formula derived from minimizing the total unusefulness
    a = (sum_y - sum_x) / (N + sum_x2 - sum_xy)
    
    return a

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