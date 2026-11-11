import sys
from itertools import combinations

def count_intersections(n, poles):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def do_intersect(p1, q1, p2, q2):
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(p1, p2, q1):
            return True
        if o2 == 0 and on_segment(p1, q2, q1):
            return True
        if o3 == 0 and on_segment(p2, p1, q2):
            return True
        if o4 == 0 and on_segment(p2, q1, q2):
            return True

        return False

    def on_segment(p, q, r):
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    intersections = 0
    for (p1, q1), (p2, q2) in combinations(combinations(poles, 2), 2):
        if do_intersect(p1, q1, p2, q2):
            intersections += 1

    return intersections

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    poles = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    
    result = count_intersections(n, poles)
    print(result)

if __name__ == "__main__":
    main()