import sys

def min_performance_duration(a, b, c, d):
    # Calculate the initial distances between each pair of ropewalkers
    dist_ab = abs(a - b)
    dist_bc = abs(b - c)
    dist_ca = abs(c - a)
    
    # If all distances are already at least d, the performance is already done
    if dist_ab >= d and dist_bc >= d and dist_ca >= d:
        return 0
    
    # Calculate the maximum distance that needs to be increased
    max_dist = max(dist_ab, dist_bc, dist_ca)
    
    # The minimum duration is the difference between the maximum distance and d
    return max(0, max_dist - d)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    a = int(data[0])
    b = int(data[1])
    c = int(data[2])
    d = int(data[3])
    result = min_performance_duration(a, b, c, d)
    print(result)

if __name__ == "__main__":
    main()