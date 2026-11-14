import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    x = [int(input_data[i+1]) for i in range(n)]

    # Create segments as (min_x, max_x)
    segments = []
    for i in range(n - 1):
        a, b = x[i], x[i+1]
        if a > b:
            a, b = b, a
        segments.append((a, b))

    # Check all pairs of segments for intersection
    # Two semi-circles intersect if and only if their intervals overlap partially
    # i.e., one starts inside the other and ends outside, or vice versa.
    # They do NOT intersect if one is completely inside the other or completely outside.
    # They do NOT intersect if they share an endpoint (since points are distinct and order matters, 
    # but geometrically touching at endpoints of diameter doesn't count as self-intersection of the arc itself 
    # in the context of this problem's "crossing" definition).
    
    # Condition for intersection between (a1, b1) and (a2, b2) where a1 < b1 and a2 < b2:
    # They intersect if: a1 < a2 < b1 < b2 OR a2 < a1 < b2 < b1
    # This is equivalent to: max(a1, a2) < min(b1, b2) AND not (a1 <= a2 and b2 <= b1) AND not (a2 <= a1 and b1 <= b2)
    # Simpler logic: 
    # Overlap exists if max(a1, a2) < min(b1, b2)
    # But we must exclude the case where one is fully contained in the other.
    # Containment cases:
    # 1. a1 <= a2 and b2 <= b1 (segment 2 inside segment 1)
    # 2. a2 <= a1 and b1 <= b2 (segment 1 inside segment 2)
    
    has_intersection = False
    for i in range(n - 1):
        a1, b1 = segments[i]
        for j in range(i + 1, n - 1):
            a2, b2 = segments[j]
            
            # Check if intervals overlap
            if max(a1, a2) < min(b1, b2):
                # Check if one is fully contained in the other
                contained = False
                if a1 <= a2 and b2 <= b1:
                    contained = True
                if a2 <= a1 and b1 <= b2:
                    contained = True
                
                if not contained:
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