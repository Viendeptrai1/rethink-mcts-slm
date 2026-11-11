import sys
import bisect

def main():
    import sys
    import bisect

    def readints():
        return list(map(int, sys.stdin.readline().split()))

    n = int(sys.stdin.readline())
    xs = []
    ys = []
    for _ in range(n):
        x, y = readints()
        xs.append(x)
        ys.append(y)
    d = int(sys.stdin.readline())

    xs.sort()
    ys.sort()

    def median(lst):
        mid = len(lst) // 2
        if len(lst) % 2 == 0:
            return (lst[mid - 1] + lst[mid]) // 2
        else:
            return lst[mid]

    x_median = median(xs)
    y_median = median(ys)

    total_distance = 0
    for x in xs:
        total_distance += abs(x - x_median)
    for y in ys:
        total_distance += abs(y - y_median)

    max_distance = 0
    for x in xs:
        max_distance = max(max_distance, abs(x - x_median))
    for y in ys:
        max_distance = max(max_distance, abs(y - y_median))

    if max_distance <= d:
        print(total_distance)
    else:
        print("impossible")

if __name__ == "__main__":
    main()