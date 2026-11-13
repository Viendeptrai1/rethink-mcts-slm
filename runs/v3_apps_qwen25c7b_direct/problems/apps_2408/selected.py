def count_intersecting_wires(n, poles):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def on_segment(p, q, r):
        if (min(q[0], r[0]) <= p[0] <= max(q[0], r[0])) and \
           (min(q[1], r[1]) <= p[1] <= max(q[1], r[1])):
            return True
        return False

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

    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if do_intersect(poles[i], poles[j], poles[k], poles[l]):
                        count += 1
    return count

import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
poles = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
print(count_intersecting_wires(n, poles))