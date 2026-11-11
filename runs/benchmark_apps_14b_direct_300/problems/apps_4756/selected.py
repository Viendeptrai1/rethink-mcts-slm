import sys
import math

def find_min_a(N, points):
    total_x = sum(x for x, y in points)
    total_y = sum(y for x, y in points)
    
    # Calculate the optimal a
    a = (total_y - total_x) / N
    
    return a

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = []
    
    for i in range(N):
        x = int(data[2 * i + 1])
        y = int(data[2 * i + 2])
        points.append((x, y))
    
    a = find_min_a(N, points)
    print(f"{a:.6f}")

if __name__ == "__main__":
    main()