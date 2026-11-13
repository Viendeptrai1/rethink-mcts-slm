import sys

def find_optimal_a(N, points):
    points.sort()
    
    def calculate_unusefulness(a):
        return sum((p[1] - (p[0] + a)) ** 2 for p in points)
    
    left = min(p[1] - p[0] for p in points) - 10**-6
    right = max(p[1] - p[0] for p in points) + 10**-6
    while right - left > 10**-6:
        mid1 = (left * 2 + right) / 3
        mid2 = (left + right * 2) / 3
        if calculate_unusefulness(mid1) < calculate_unusefulness(mid2):
            right = mid2
        else:
            left = mid1
    
    return (left + right) / 2

input = sys.stdin.read
data = input().split()

N = int(data[0])
points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

result = find_optimal_a(N, points)
print(f"{result:.6f}")