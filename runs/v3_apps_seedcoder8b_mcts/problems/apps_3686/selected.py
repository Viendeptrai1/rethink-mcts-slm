def can_hit_all_targets(N, targets):
    if N <= 2:
        return "success"
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    slopes = set()
    for i in range(N):
        for j in range(i + 1, N):
            x1, y1 = targets[i]
            x2, y2 = targets[j]
            dx = x2 - x1
            dy = y2 - y1
            g = gcd(dx, dy)
            slope = (dy // g, dx // g)
            slopes.add(slope)
            if len(slopes) > 2:
                return "failure"
    
    return "success"

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