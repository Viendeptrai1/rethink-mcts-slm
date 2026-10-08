import sys
import bisect

def main():
    import sys
    import bisect

    def readints():
        return list(map(int, sys.stdin.readline().split()))

    n = readints()[0]
    points = [readints() for _ in range(n)]
    d = readints()[0]

    xs = sorted([p[0] for p in points])
    ys = sorted([p[1] for p in points])

    def median(lst):
        mid = len(lst) // 2
        if len(lst) % 2 == 0:
            return (lst[mid - 1] + lst[mid]) // 2
        else:
            return lst[mid]

    med_x = median(xs)
    med_y = median(ys)

    def total_distance(x, y):
        return sum(abs(px - x) + abs(py - y) for px, py in points)

    def is_valid(x, y):
        return all(abs(px - x) + abs(py - y) <= d for px, py in points)

    min_dist = float('inf')
    found = False

    for x in [med_x - 1, med_x, med_x + 1]:
        for y in [med_y - 1, med_y, med_y + 1]:
            if is_valid(x, y):
                dist = total_distance(x, y)
                if dist < min_dist:
                    min_dist = dist
                    found = True

    if found:
        print(min_dist)
    else:
        print("impossible")

if __name__ == "__main__":
    main()