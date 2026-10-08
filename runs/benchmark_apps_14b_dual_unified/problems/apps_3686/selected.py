import sys
from collections import defaultdict

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]
    
    if N <= 2:
        print("success")
        return
    
    def count_collinear(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        g = gcd(dx, dy)
        slope = (dx // g, dy // g)
        intercept = (p1[0] * slope[1] - p1[1] * slope[0]) // (slope[0] * slope[0] + slope[1] * slope[1])
        return slope, intercept
    
    max_collinear = 0
    slopes = defaultdict(int)
    
    for i in range(N):
        for j in range(i+1, N):
            slope, intercept = count_collinear(points[i], points[j])
            slopes[(slope, intercept)] += 1
            max_collinear = max(max_collinear, slopes[(slope, intercept)])
    
    if max_collinear >= N:
        print("success")
    else:
        sorted_slopes = sorted(slopes.values(), reverse=True)
        if len(sorted_slopes) > 1 and sorted_slopes[0] + sorted_slopes[1] >= N:
            print("success")
        else:
            print("failure")

if __name__ == "__main__":
    main()