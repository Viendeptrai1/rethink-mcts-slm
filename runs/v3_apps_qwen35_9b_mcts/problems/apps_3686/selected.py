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

    points = []
    for _ in range(n):
        x = int(next(iterator))
        y = int(next(iterator))
        points.append((x, y))

    if n <= 2:
        print("success")
        return

    # We need to find two lines that cover all points.
    # Strategy:
    # 1. Take the first three points: p0, p1, p2.
    # 2. These three points must be covered by the two lines.
    #    There are two main cases for how they are distributed:
    #    Case A: All three are collinear. Then one line covers p0, p1, p2. The second line can cover any remaining point (or be empty if n=3 and they are collinear, but we need to cover all). Actually, if p0, p1, p2 are collinear, we can form Line1 with them. Then we just need to check if all other points lie on Line1 or on some Line2 defined by p0 and some other point p_k (where p_k is not on Line1).
    #    Case B: They are not collinear. Then each pair defines a line. Specifically, Line1 must contain p0 and p1, and Line2 must contain p0 and p2 (or p1 and p2, etc.). Since p0, p1, p2 are not collinear, p0 is the intersection point of the two lines. One line goes through p0-p1, the other through p0-p2. We then verify if all points lie on either line p0-p1 or line p0-p2.
    
    # Let's refine the logic to be robust:
    # We know the solution must cover p0. So p0 is on Line A or Line B.
    # Consider the set of points. If we pick p0 and p1, they define a candidate line L1.
    # If we pick p0 and p2, they define a candidate line L2.
    # If p0, p1, p2 are collinear, then L1 == L2. In this case, we have one line covering p0, p1, p2. We need to find a second line that covers the rest. The second line must pass through p0 (since p0 is on the first line, and if the second line doesn't pass through p0, then p0 is only on the first line, which is fine, but wait... if p0, p1, p2 are collinear, we can have Line1 = line(p0, p1). Then we need to cover the remaining points. The remaining points must be coverable by a single line. This single line could pass through p0 or not. However, if it doesn't pass through p0, then p0 is only on Line1. But we have 2 shots.
    # Actually, a simpler approach:
    # The two lines must cover all points.
    # Consider the first point p0. It must belong to one of the lines, say Line A.
    # Consider the second point p1. It must belong to Line A or Line B.
    # Consider the third point p2. It must belong to Line A or Line B.
    
    # Scenario 1: p0, p1, p2 are collinear.
    #   Then Line A could be the line containing p0, p1, p2.
    #   Then all other points must lie on Line A or on some Line B.
    #   If all other points lie on Line A, success.
    #   If not, then Line B must cover the points not on Line A. Since Line B is a straight line, all points not on Line A must be collinear.
    #   Also, Line B could pass through p0. If Line B passes through p0, then p0 is on both lines.
    #   So if p0, p1, p2 are collinear:
    #     Check if all points are on line(p0, p1). If yes -> success.
    #     If no, collect points not on line(p0, p1). If this set is empty -> success (already covered).
    #     If not empty, check if all these remaining points are collinear. If yes -> success.
    #     Wait, is it possible that Line A does NOT contain p1? 
    #     If p0, p1, p2 are collinear, we could have Line A = line(p0, p2) and Line B = line(p1, p3) for some p3. But since p0, p1, p2 are collinear, line(p0, p2) is the same as line(p0, p1). So effectively, the line containing p0, p1, p2 is unique.
    #     So if p0, p1, p2 are collinear, one of the lines MUST be the line containing p0, p1, p2. Why? Because p0, p1, p2 are 3 points. If they are on two lines, by Pigeonhole Principle, at least 2 of them are on the same line. Since they are collinear, all 3 are on that line. So one line is fixed as line(p0, p1).
    #     Therefore, if p0, p1, p2 are collinear, we just check:
    #       1. Are all points on line(p0, p1)? -> success.
    #       2. If not, let S be the set of points not on line(p0, p1). Are all points in S collinear? -> success.
    #       3. Otherwise failure.
    
    # Scenario 2: p0, p1, p2 are NOT collinear.
    #   Then p0, p1, p2 cannot all be on the same line.
    #   So the two lines must split these three points.
    #   Possible splits:
    #     - Line A has {p0, p1}, Line B has {p2}. (And Line B might have more points).
    #     - Line A has {p0, p2}, Line B has {p1}.
    #     - Line A has {p1, p2}, Line B has {p0}.
    #   In all these cases, the intersection of the two lines must be one of the points (p0, p1, or p2) OR the lines are parallel (but if they are parallel and cover 3 non-collinear points, it's impossible because 3 non-collinear points require 2 lines, and if lines are parallel, they don't intersect, so one line can have at most 2 of the points? No. If lines are parallel, they are distinct. p0 on L1, p1 on L1, p2 on L2. This works. But if p0, p1, p2 are not collinear, can we have L1 = line(p0, p1) and L2 = line(p2, something)? Yes.
    #   However, note that if p0, p1, p2 are not collinear, then p0, p1 define a line L1, and p0, p2 define a line L2. These two lines intersect at p0.
    #   Could the solution be L1 = line(p0, p1) and L2 = line(p1, p2)? They intersect at p1.
    #   Could the solution be L1 = line(p0, p2) and L2 = line(p1, p2)? They intersect at p2.
    #   Are there other possibilities? What if L1 contains p0 and p1, and L2 contains p2 and some other point p_k, but L2 does not pass through p0 or p1? Yes, that's possible. But then p0 and p1 are on L1, p2 is on L2.
    #   The key observation: Since p0, p1, p2 are not collinear, at least two of them must be on one line, and the third on the other.
    #   So the two lines are determined by pairs: (p0, p1) and (p0, p2) -> intersect at p0.
    #   OR (p0, p1) and (p1, p2) -> intersect at p1.
    #   OR (p0, p2) and (p1, p2) -> intersect at p2.
    #   Wait, is it possible that the two lines are parallel?
    #     If L1 and L2 are parallel, then they never intersect.
    #     p0, p1, p2 are not collinear.
    #     Suppose p0, p1 on L1. Then p2 must be on L2.
    #     Can we have p0, p1 on L1 and p2 on L2? Yes.
    #     But what if there is a point p3 that is on L1? Then L1 is defined by p0, p1, p3.
    #     The issue is: if p0, p1, p2 are not collinear, we don't know which pair forms a line.
    #     However, we can try all 3 possibilities:
    #       Possibility 1: Line A = line(p0, p1), Line B = line(p0, p2). Check if all points are on A or B.
    #       Possibility 2: Line A = line(p0, p1), Line B = line(p1, p2). Check if all points are on A or B.
    #       Possibility 3: Line A = line(p0, p2), Line B = line(p1, p2). Check if all points are on A or B.
    #     Is it possible that the correct lines are line(p0, p1) and line(p2, p3) where p3 is some other point, and p0, p1, p2 are not collinear?
    #       If Line A = line(p0, p1) and Line B = line(p2, p3).
    #       Then p0, p1 are on A. p2, p3 are on B.
    #       What about p2? It is on B.
    #       In this scenario, p0, p1, p2 are not collinear (given).
    #       But notice that in this scenario, the line containing p0 and p1 is A, and the line containing p2 is B.
    #       Does B have to pass through p0 or p1? Not necessarily.
    #       However, consider the set of points. If we assume Line A = line(p0, p1), then all points not on A must be collinear (on Line B).
    #       So, if we fix Line A = line(p0, p1), we can check if the remaining points (those not on A) are collinear. If they are, then success.
    #       Similarly, we can try fixing Line A = line(p0, p2) and check if the rest are collinear.
    #       And Line A = line(p1, p2) and check if the rest are collinear.
    #     This covers all cases because one of the lines MUST contain at least two of the first three points (p0, p1, p2). Why? Because there are 3 points and 2 lines. By PHP, one line has at least 2 points.
    #     So the algorithm:
    #       Try candidate lines formed by pairs from {p0, p1, p2}:
    #         1. L = line(p0, p1). Check if all points are on L or if the points not on L are collinear.
    #         2. L = line(p0, p2). Check if all points are on L or if the points not on L are collinear.
    #         3. L = line(p1, p2). Check if all points are on L or if the points not on L are collinear.
    #       If any of these checks pass, return "success".
    #       Otherwise "failure".
    
    # Helper to check if a point is on a line defined by two points (x1, y1) and (x2, y2)
    # Using cross product: (x - x1)*(y2 - y1) - (y - y1)*(x2 - x1) == 0
    def is_on_line(px, py, x1, y1, x2, y2):
        return (px - x1) * (y2 - y1) == (py - y1) * (x2 - x1)

    # Helper to check if a list of points are collinear
    def are_collinear(pts):
        if len(pts) <= 2:
            return True
        x1, y1 = pts[0]
        x2, y2 = pts[1]
        for i in range(2, len(pts)):
            if not is_on_line(pts[i][0], pts[i][1], x1, y1, x2, y2):
                return False
        return True

    # Try each pair from the first three points as the first line
    candidates = [
        (points[0], points[1]),
        (points[0], points[2]),
        (points[1], points[2])
    ]

    for p_a, p_b in candidates:
        xa, ya = p_a
        xb, yb = p_b
        
        # Define the line
        # Separate points into those on the line and those not
        on_line = []
        off_line = []
        
        for i in range(n):
            if is_on_line(points[i][0], points[i][1], xa, ya, xb, yb):
                on_line.append(points[i])
            else:
                off_line.append(points[i])
        
        # If all points are on this line, success
        if len(off_line) == 0:
            print("success")
            return
        
        # If not, check if all off_line points are collinear
        if are_collinear(off_line):
            print("success")
            return

    print("failure")

if __name__ == "__main__":
    solve()