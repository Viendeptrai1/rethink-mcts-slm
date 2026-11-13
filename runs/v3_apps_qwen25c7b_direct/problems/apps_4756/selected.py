import sys

def find_min_a(N, points):
    points.sort()
    median_y = points[N // 2][1]
    return median_y - points[N // 2][0]

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = [(int(data[2 * i + 1]), int(data[2 * i + 2])) for i in range(N)]
    
    result = find_min_a(N, points)
    print(f"{result:.6f}")