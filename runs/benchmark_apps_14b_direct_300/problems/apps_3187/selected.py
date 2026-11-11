import sys
import bisect

def main():
    import sys
    import bisect

    def readints():
        return list(map(int, sys.stdin.readline().split()))

    n = readints()[0]
    xs = []
    ys = []
    for _ in range(n):
        x, y = readints()
        xs.append(x)
        ys.append(y)
    d = readints()[0]

    xs.sort()
    ys.sort()

    def median(lst):
        return lst[len(lst) // 2]

    med_x = median(xs)
    med_y = median(ys)

    def check(x, y):
        return all(abs(x - cx) + abs(y - cy) <= d for cx, cy in zip(xs, ys))

    if check(med_x, med_y):
        total_distance = sum(abs(med_x - x) + abs(med_y - y) for x, y in zip(xs, ys))
        print(total_distance)
    else:
        print("impossible")

if __name__ == "__main__":
    main()