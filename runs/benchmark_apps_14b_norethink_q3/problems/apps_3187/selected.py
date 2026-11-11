import sys
import bisect

def main():
    import sys
    import bisect
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n = read_ints()[0]
    xs = []
    ys = []
    for _ in range(n):
        x, y = read_ints()
        xs.append(x)
        ys.append(y)
    d = read_ints()[0]
    
    xs.sort()
    ys.sort()
    
    def median(lst):
        return lst[len(lst) // 2]
    
    def total_distance(x, y):
        return sum(abs(x - xi) + abs(y - yi) for xi, yi in zip(xs, ys))
    
    def check(x, y):
        return all(abs(x - xi) + abs(y - yi) <= d for xi, yi in zip(xs, ys))
    
    min_total_distance = float('inf')
    found = False
    
    for x in [median(xs)]:
        left = bisect.bisect_left(xs, x - d)
        right = bisect.bisect_right(xs, x + d)
        for y in [median(ys[left:right])]:
            if check(x, y):
                min_total_distance = min(min_total_distance, total_distance(x, y))
                found = True
    
    if found:
        print(min_total_distance)
    else:
        print("impossible")

if __name__ == "__main__":
    main()