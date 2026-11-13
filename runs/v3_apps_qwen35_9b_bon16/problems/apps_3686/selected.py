import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    coords = []
    for _ in range(n):
        x = int(next(iterator))
        y = int(next(iterator))
        coords.append((x, y))

    if n <= 2:
        print("success")
        return

    # Check if all points are collinear (1 shot is enough)
    # Use the first point as reference to check others
    p0 = coords[0]
    p1 = coords[1]
    
    # Calculate dx, dy for the first segment
    dx0 = p1[0] - p0[0]
    dy0 = p1[1] - p0[1]
    
    # Check if dx0 and dy0 are both zero (should not happen per problem statement: no two targets at same coords)
    if dx0 == 0 and dy0 == 0:
        # All points are the same? Problem says no two targets at same coords, so this implies n=1 which is handled.
        print("success")
        return

    all_collinear = True
    for i in range(2, n):
        pi = coords[i]
        # Cross product: (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1) should be 0
        cross = (p1[0] - p0[0]) * (pi[1] - p0[1]) - (p1[1] - p0[1]) * (pi[0] - p0[0])
        if cross != 0:
            all_collinear = False
            break
    
    if all_collinear:
        print("success")
        return

    # If not all collinear, we need 2 lines.
    # The two lines must cover all points.
    # Strategy:
    # 1. Identify two candidate points that MUST be on different lines?
    # Actually, a known property: If we can cover all points with 2 lines, then any 3 points that are not collinear cannot all be on the same line.
    # More specifically: Take the first 3 points. They form a triangle (since not all collinear).
    # At least two of these three points must belong to different lines if the total set requires 2 lines?
    # Not necessarily. Consider points A, B, C forming a triangle. Maybe A and B are on line 1, C and D on line 2.
    # However, if we pick ANY 3 points that are NOT collinear, say P_i, P_j, P_k.
    # In the 2-line scenario, these 3 points must be distributed such that at least two are on one line and one on the other, OR one on one and two on the other.
    # Actually, the key insight for "can be covered by 2 lines" is:
    # Pick the first point (index 0). It must be on one of the lines, say Line A.
    # Pick the second point (index 1). It must be on one of the lines.
    # Case 1: P0 and P1 are on the same line. Then Line A is defined by P0 and P1.
    #   We remove all points collinear with P0-P1. If the remaining points are collinear, then success.
    # Case 2: P0 and P1 are on different lines.
    #   Then Line A passes through P0 and some other point, and Line B passes through P1.
    #   But we don't know the other points.
    #
    # Alternative robust approach:
    # If the points can be covered by 2 lines, then there exists a pair of points (i, j) such that:
    # All other points are either on line(i, j) OR on some other line L2.
    # This implies that if we fix two points to define the first line, we can check if the rest are collinear.
    # But iterating all pairs is O(N^2). N=100,000 -> too slow.
    #
    # Optimization:
    # Consider the first point P0. It must belong to either Line1 or Line2.
    # Consider the second point P1. It must belong to either Line1 or Line2.
    #
    # Scenario A: P0 and P1 are on the SAME line (Line A).
    #   Define Line A by P0 and P1.
    #   Check if all remaining points are collinear with Line A. If yes, done (1 shot needed, which is <= 2).
    #   If not, then the points NOT on Line A must all lie on a single second line (Line B).
    #   So, collect all points not on Line A. Check if they are collinear.
    #
    # Scenario B: P0 and P1 are on DIFFERENT lines.
    #   Then Line A passes through P0, and Line B passes through P1.
    #   Which other points are on Line A? At least one more point (unless N=2, but we know N>=3 and not all collinear).
    #   Actually, if P0 is on Line A and P1 is on Line B, then any point Pk that is collinear with P0 and some Pj (where Pj is also on Line A) defines Line A.
    #   How to find Line A and Line B efficiently?
    #   Notice that if P0 and P1 are on different lines, then the set of points on Line A includes P0 and at least one other point (say Pk).
    #   The set of points on Line B includes P1 and at least one other point (say Pl).
    #   If we assume P0 is on Line A, then Line A is determined by P0 and some Pk.
    #   If we assume P1 is on Line B, then Line B is determined by P1 and some Pl.
    #   But we don't know Pk or Pl.
    #
    # However, there is a symmetry. If a solution exists, then EITHER:
    # 1. The line containing P0 also contains P1. (Covered by Scenario A)
    # 2. The line containing P0 does NOT contain P1.
    #    In this case, P0 is on Line A, P1 is on Line B.
    #    Consider the third point P2.
    #    P2 must be on either Line A or Line B.
    #    Subcase 2a: P2 is on Line A. Then Line A is defined by P0 and P2. We can check if the rest are collinear with P0-P2, OR if the rest (excluding those on P0-P2) are collinear with P1 (since P1 is on Line B, and if Line B only has P1 and the remaining points, they must be collinear with P1? Wait, Line B needs at least 2 points to be defined uniquely if N>2? Or Line B could be defined by P1 and any other point not on Line A).
    #       Actually, if P0 and P2 are on Line A, then Line A = line(P0, P2).
    #       Remove all points on Line A. The remaining points must be collinear (forming Line B). Note that P1 is in this set.
    #    Subcase 2b: P2 is on Line B. Then Line B is defined by P1 and P2.
    #       Remove all points on Line B. The remaining points must be collinear (forming Line A). Note that P0 is in this set.
    #
    # So, if P0 and P1 are on different lines, we can test:
    # Option 1: Assume Line A = line(P0, P2). Check if rest are collinear.
    # Option 2: Assume Line B = line(P1, P2). Check if rest are collinear.
    #
    # Wait, what if P0, P1, P2 are all on different lines? Impossible with only 2 lines.
    # So by Pigeonhole Principle, among any 3 points, at least 2 must be on the same line.
    # Therefore, we only need to check pairs from the first 3 points?
    # Actually, we can just try:
    # 1. Line defined by (P0, P1). Check if rest collinear.
    # 2. Line defined by (P0, P2). Check if rest collinear.
    # 3. Line defined by (P1, P2). Check if rest collinear.
    # If any of these works (meaning the points NOT on this line are collinear), then YES.
    # Why?
    # - If all 3 are on the same line, then case 1 catches it (rest are all collinear on that line).
    # - If P0, P1 on Line A, P2 on Line B:
    #     Case 1 (P0,P1): Rest includes P2 and others on Line B. We check if "Rest" are collinear. Since P2 is on Line B, and all other rest are on Line B (because only 2 lines), then yes.
    #     Case 2 (P0,P2): Line A candidate. Rest includes P1 (on Line A? No, P1 is on Line A with P0) and others. If P0 and P2 are on different lines, then line(P0, P2) is neither Line A nor Line B (unless P0, P2 are on the same line, which contradicts assumption). So this specific line check might fail if P0 and P2 are on different lines.
    #     BUT, we also check Case 3 (P1, P2). If P1 and P2 are on different lines, this also defines a new line.
    #
    # Let's refine:
    # The correct logic is:
    # Try every pair from the first 3 points (indices 0, 1, 2).
    # For each pair (i, j):
    #   Define Line L = line(Pi, Pj).
    #   Collect all points NOT on L.
    #   Check if these remaining points are collinear.
    #   If yes, return "success".
    #
    # Is it sufficient to check only pairs from the first 3 points?
    # Yes. Because if a valid configuration exists with 2 lines, then among the first 3 points, at least two must lie on the same line (Pigeonhole: 3 points, 2 lines -> at least one line has >=2 points).
    # Let the two points on the same line be Pi and Pj.
    # Then the line defined by Pi and Pj is exactly one of the two lines (or a subset of it).
    # The remaining points (including the third point from the set of 3) must lie on the other line (or be collinear with Pi-Pj).
    # So checking the pair (Pi, Pj) will result in the "remaining points" being exactly the set of points on the second line, which are collinear.
    #
    # Algorithm:
    # 1. Read points.
    # 2. If N <= 2, success.
    # 3. Check if all N points are collinear. If yes, success.
    # 4. Otherwise, consider points P0, P1, P2.
    #    Try pairs (0,1), (0,2), (1,2).
    #    For each pair (a, b):
    #       Define line through Pa and Pb.
    #       Identify all points NOT on this line.
    #       Check if these "not on line" points are collinear.
    #       If yes, return "success".
    # 5. If none work, return "failure".

    # Helper to check collinearity of a list of points
    def check_collinear(points):
        if len(points) <= 2:
            return True
        # Take first two to define line
        p0 = points[0]
        p1 = points[1]
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        for i in range(2, len(points)):
            p = points[i]
            # Cross product
            if dx * (p[1] - p0[1]) != dy * (p[0] - p0[0]):
                return False
        return True

    # Check all collinear first
    # Re-use logic: check if all points are on line(P0, P1)
    # But wait, we already did that in "all_collinear" check.
    # Actually, the "all_collinear" check above is robust.
    if all_collinear:
        print("success")
        return

    # If not all collinear, we need to check the 3-point combinations.
    # Points to consider: 0, 1, 2.
    # Pairs: (0,1), (0,2), (1,2)
    
    candidates = [
        (0, 1),
        (0, 2),
        (1, 2)
    ]

    for i, j in candidates:
        p_i = coords[i]
        p_j = coords[j]
        
        # Define line by p_i and p_j
        # Check which points are NOT on this line
        not_on_line = []
        for k in range(n):
            if k == i or k == j:
                continue
            pk = coords[k]
            # Cross product check
            # (pj.x - pi.x)*(pk.y - pi.y) - (pj.y - pi.y)*(pk.x - pi.x) == 0
            dx = p_j[0] - p_i[0]
            dy = p_j[1] - p_i[1]
            cross = dx * (pk[1] - p_i[1]) - dy * (pk[0] - p_i[0])
            if cross != 0:
                not_on_line.append(pk)
        
        # Now check if not_on_line is collinear
        if check_collinear(not_on_line):
            print("success")
            return

    print("failure")

if __name__ == "__main__":
    solve()