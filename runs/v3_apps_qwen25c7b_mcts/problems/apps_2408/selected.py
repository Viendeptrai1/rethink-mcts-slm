from itertools import combinations

def count_intersections(n, poles):
    def get_slope(p1, p2):
        if p1[0] == p2[0]:
            return float('inf')
        return (p1[1] - p2[1]) / (p1[0] - p2[0])

    def get_intercept(p, slope):
        if slope == float('inf'):
            return p[0]
        return p[1] - slope * p[0]

    slopes = {}
    intercepts = {}

    for p1, p2 in combinations(poles, 2):
        slope = get_slope(p1, p2)
        intercept = get_intercept(p1, slope)

        if (slope, intercept) in slopes:
            slopes[(slope, intercept)].append((p1, p2))
        else:
            slopes[(slope, intercept)] = [(p1, p2)]

    intersection_count = 0

    for key, value in slopes.items():
        if len(value) > 1:
            intersection_count += len(value) * (len(value) - 1) // 2

    return intersection_count

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    poles = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(n)]
    
    result = count_intersections(n, poles)
    print(result)