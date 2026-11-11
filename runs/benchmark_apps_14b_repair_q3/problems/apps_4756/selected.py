import sys
import math

def find_min_a(N, points):
    total_x = sum(x for x, y in points)
    total_y = sum(y for x, y in points)
    
    # Calculate the optimal 'a' using the formula derived from minimizing the sum of squared distances
    a = (total_y - total_x) / N
    
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
    
    a = find_min_a(N, points)
    print(f"{a:.6f}")

if __name__ == "__main__":
    main()