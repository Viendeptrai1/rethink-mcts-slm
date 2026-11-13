def can_hit_all_targets(N, targets):
    if N <= 2:
        return "success"
    
    # Calculate slopes and intercepts for each pair of points
    slopes = {}
    for i in range(N):
        for j in range(i + 1, N):
            x1, y1 = targets[i]
            x2, y2 = targets[j]
            if x1 == x2:
                slope = float('inf')
                intercept = x1
            else:
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - slope * x1
            if (slope, intercept) not in slopes:
                slopes[(slope, intercept)] = 0
            slopes[(slope, intercept)] += 1
    
    # Check if any line has more than 1 target
    for count in slopes.values():
        if count > 1:
            return "success"
    
    return "failure"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    targets = []
    index = 1
    for _ in range(N):
        x = int(data[index])
        y = int(data[index + 1])
        targets.append((x, y))
        index += 2
    
    result = can_hit_all_targets(N, targets)
    print(result)