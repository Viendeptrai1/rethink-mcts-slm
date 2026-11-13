from itertools import combinations

def count_intersecting_wires(n, coordinates):
    def orientation(p, q, r):
        return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    def on_segment(p, q, r):
        return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
                min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

    def intersect(p1, q1, p2, q2):
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(p1, p2, q1): return True
        if o2 == 0 and on_segment(p1, q2, q1): return True
        if o3 == 0 and on_segment(p2, p1, q2): return True
        if o4 == 0 and on_segment(p2, q1, q2): return True

        return False

    count = 0
    for (p1, p2), (q1, q2) in combinations(combinations(coordinates, 2), 2):
        if intersect(p1, p2, q1, q2):
            count += 1

    return count

if __name__ == "__main__":
    n = int(input())
    coordinates = [tuple(map(int, input().split())) for _ in range(n)]
    result = count_intersecting_wires(n, coordinates)
    print(result)