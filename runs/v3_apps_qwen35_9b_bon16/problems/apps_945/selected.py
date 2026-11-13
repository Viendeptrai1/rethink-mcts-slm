import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        x = []
        for _ in range(n):
            x.append(int(next(iterator)))
    except StopIteration:
        return

    # If there are fewer than 4 points, no intersection is possible since we need at least two arcs to intersect.
    # Actually, with 3 points we have 2 arcs. Two arcs can only intersect if they cross, which requires 4 endpoints involved in a specific way.
    # But logically, with n < 4, we can't form a closed loop or a crossing like X.
    # Let's stick to the general logic below, it handles small n naturally.

    # We need to check for intersections between consecutive semicircles.
    # Semicircle i connects x[i] and x[i+1].
    # Semicircle j connects x[j] and x[j+1].
    # They intersect if and only if the intervals (min(x[i], x[i+1]), max(x[i], x[i+1])) and 
    # (min(x[j], x[j+1]), max(x[j], x[j+1])) overlap, but neither is contained within the other.
    # Since the arcs are above the axis, if the intervals are disjoint, arcs don't touch.
    # If one interval is strictly inside the other, the inner arc is below the outer arc, so no intersection.
    # Intersection happens if the intervals "cross" (e.g., [a, b] and [b, c] where a < b < c -> no, they meet at b).
    # Wait, the problem says "distinct points". So endpoints are distinct.
    # Intersection occurs if the open intervals (min1, max1) and (min2, max2) have a non-empty intersection,
    # and neither interval contains the other completely.
    # Mathematically: Let I1 = (L1, R1) and I2 = (L2, R2) with L1 < R1 and L2 < R2.
    # They intersect iff L1 < L2 < R1 < R2 or L2 < L1 < R2 < R1.
    # Basically, the order of endpoints on the line must be interleaved.

    has_intersection = False

    # Generate arcs: each arc is defined by (L, R) where L < R
    arcs = []
    for i in range(n - 1):
        u, v = x[i], x[i+1]
        if u > v:
            u, v = v, u
        arcs.append((u, v))

    num_arcs = len(arcs)
    for i in range(num_arcs):
        L1, R1 = arcs[i]
        for j in range(i + 1, num_arcs):
            L2, R2 = arcs[j]
            
            # Check for intersection
            # Condition 1: Intervals must overlap (not disjoint)
            # Overlap exists if max(L1, L2) < min(R1, R2)
            # Condition 2: Neither interval contains the other.
            # If L1 < L2 < R1 < R2 -> Intersect
            # If L2 < L1 < R2 < R1 -> Intersect
            # If L1 < L2 < R2 < R1 -> No (I2 inside I1)
            # If L2 < L1 < R1 < R2 -> No (I1 inside I2)
            # If disjoint -> No

            if not (L1 < L2 < R1 < R2) and not (L2 < L1 < R2 < R1):
                continue
            
            has_intersection = True
            break
        if has_intersection:
            break

    if has_intersection:
        print("yes")
    else:
        print("no")

if __name__ == "__main__":
    solve()