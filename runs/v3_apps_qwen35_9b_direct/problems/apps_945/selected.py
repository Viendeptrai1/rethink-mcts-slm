import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    x = []
    for i in range(n):
        x.append(int(input_data[1 + i]))

    # We need to check if any two consecutive semi-circles intersect.
    # Semi-circle i connects x[i] and x[i+1].
    # Semi-circle j connects x[j] and x[j+1].
    # Two semi-circles intersect if and only if their intervals overlap in a specific way.
    # Let interval i be [min(x[i], x[i+1]), max(x[i], x[i+1])]
    # Let interval j be [min(x[j], x[j+1]), max(x[j], x[j+1])]
    # They intersect if:
    # 1. The intervals overlap (not just touching at endpoints, but sharing interior points)
    #    AND
    # 2. The order of endpoints is "crossed".
    # Specifically, if we have points A, B for arc 1 and C, D for arc 2.
    # Without loss of generality, assume A < B and C < D.
    # The arcs intersect if and only if:
    # A < C < B < D  OR  C < A < D < B
    # Note: If they share an endpoint (e.g., B == C), they touch but do not "cross" in a way that creates a self-intersection of the path itself in the context of this problem (the path is continuous). The problem asks if the line intersects itself. Touching at a common point (like a chain) is not a self-intersection of the curve with itself in the sense of crossing. The examples confirm this: 0-10 and 5-15 cross. 0-15 and 5-10 do not cross (one is inside the other).
    # Wait, let's re-verify the "inside" case.
    # Case 1: 0, 10, 5, 15.
    # Arc 1: 0 to 10. Interval [0, 10].
    # Arc 2: 10 to 5. Interval [5, 10].
    # Arc 3: 5 to 15. Interval [5, 15].
    # Check Arc 1 and Arc 3: [0, 10] and [5, 15].
    # Endpoints: 0, 10 and 5, 15.
    # Order: 0 < 5 < 10 < 15. This is A < C < B < D. They cross. Output: yes. Correct.
    #
    # Case 2: 0, 15, 5, 10.
    # Arc 1: 0 to 15. Interval [0, 15].
    # Arc 2: 15 to 5. Interval [5, 15].
    # Arc 3: 5 to 10. Interval [5, 10].
    # Check Arc 1 and Arc 3: [0, 15] and [5, 10].
    # Endpoints: 0, 15 and 5, 10.
    # Order: 0 < 5 < 10 < 15. This is A < C < D < B. One interval is strictly inside the other. They do not cross.
    # Check Arc 2 and Arc 3: [5, 15] and [5, 10].
    # Endpoints: 5, 15 and 5, 10.
    # They share an endpoint (5). They touch but do not cross.
    # Output: no. Correct.

    # Algorithm:
    # Iterate over all pairs of arcs (i, j) where i < j.
    # Arc i is between x[i] and x[i+1].
    # Arc j is between x[j] and x[j+1].
    # If i and j are adjacent (j == i+1), they share an endpoint, so they don't cross.
    # For non-adjacent arcs:
    #   Let a1, a2 = x[i], x[i+1]
    #   Let b1, b2 = x[j], x[j+1]
    #   Normalize so a1 < a2 and b1 < b2.
    #   Check if (a1 < b1 < a2 < b2) or (b1 < a1 < b2 < a2).
    #   If either is true, return "yes".
    # If no such pair is found, return "no".

    for i in range(n - 1):
        for j in range(i + 1, n - 1):
            # Skip adjacent arcs as they share a vertex
            if j == i + 1:
                continue
            
            # Define intervals
            if x[i] < x[i+1]:
                a1, a2 = x[i], x[i+1]
            else:
                a1, a2 = x[i+1], x[i]
            
            if x[j] < x[j+1]:
                b1, b2 = x[j], x[j+1]
            else:
                b1, b2 = x[j+1], x[j]
            
            # Check for crossing
            # Condition 1: a1 < b1 < a2 < b2
            if a1 < b1 and b1 < a2 and a2 < b2:
                print("yes")
                return
            # Condition 2: b1 < a1 < b2 < a2
            if b1 < a1 and a1 < b2 and b2 < a2:
                print("yes")
                return

    print("no")

if __name__ == "__main__":
    solve()