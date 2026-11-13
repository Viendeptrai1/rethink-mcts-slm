def check_self_intersection(n, points):
    points.sort()
    for i in range(1, n):
        if points[i] == points[i - 1]:
            return "yes"
    return "no"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    points = list(map(int, data[1:]))
    print(check_self_intersection(n, points))