import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        xs = []
        ys = []
        for _ in range(n):
            xs.append(int(next(iterator)))
            ys.append(int(next(iterator)))
        d = int(next(iterator))
    except StopIteration:
        return

    # Sort coordinates to find medians
    xs.sort()
    ys.sort()

    # Optimal x* for minimizing sum |x - x*| is the median of xs
    # Optimal y* for minimizing sum |y - y*| is the median of ys
    # If n is odd, median is at index n//2
    # If n is even, any value between xs[n//2 - 1] and xs[n//2] (inclusive) minimizes the sum
    # We will consider the range of optimal x values [min_x_opt, max_x_opt]
    # Similarly for y: [min_y_opt, max_y_opt]

    def get_optimal_range(coords):
        m = len(coords)
        if m % 2 == 1:
            val = coords[m // 2]
            return (val, val)
        else:
            low = coords[m // 2 - 1]
            high = coords[m // 2]
            return (low, high)

    min_x_opt, max_x_opt = get_optimal_range(xs)
    min_y_opt, max_y_opt = get_optimal_range(ys)

    # The set of points (x, y) that minimize the total Manhattan distance is the Cartesian product
    # of the optimal x range and optimal y range.
    # However, we have an additional constraint: max(|x - x_i| + |y - y_i|) <= d for all i.
    # This constraint defines a region (intersection of squares rotated 45 degrees).
    # We need to find a point (x, y) in [min_x_opt, max_x_opt] x [min_y_opt, max_y_opt]
    # that also satisfies the distance constraint for all citizens, and minimizes the total distance.
    # Note: Any point in the optimal rectangle gives the same minimal total distance.
    # So we just need to check if the optimal rectangle intersects with the feasible region defined by d.
    # If it does, the answer is the minimal total distance. If not, impossible.

    # Calculate minimal total distance assuming no d constraint
    def calc_min_total_dist(coords, opt_low, opt_high):
        # Since any point in [opt_low, opt_high] gives the same sum, we can pick opt_low
        total = 0
        for x in coords:
            total += abs(x - opt_low)
        return total

    min_total_x = calc_min_total_dist(xs, min_x_opt, max_x_opt)
    min_total_y = calc_min_total_dist(ys, min_y_opt, max_y_opt)
    min_total = min_total_x + min_total_y

    # Now check feasibility: does there exist (x, y) in [min_x_opt, max_x_opt] x [min_y_opt, max_y_opt]
    # such that for all i, |x - xs[i]| + |y - ys[i]| <= d?
    # The condition |x - a| + |y - b| <= d is equivalent to:
    # x + y <= d + a + b
    # x - y <= d + a - b
    # -x + y <= d - a + b
    # -x - y <= d - a - b
    #
    # We need to find if the intersection of the rectangle R = [min_x_opt, max_x_opt] x [min_y_opt, max_y_opt]
    # and the region defined by these 4n inequalities is non-empty.
    #
    # Instead of checking all n inequalities, we can observe that the region defined by |x - x_i| + |y - y_i| <= d
    # is a square rotated by 45 degrees centered at (x_i, y_i).
    # The intersection of such squares is also a convex polygon (possibly empty).
    # We can maintain the feasible region as an intersection of such squares.
    # However, a simpler approach for this specific problem structure:
    # The optimal point must be in the rectangle R.
    # We can try to find the point in R that is "closest" to all citizens in L1 norm, but constrained by d.
    # Actually, since the objective function is constant over R, we just need ANY point in R that satisfies the d constraint.
    #
    # Let's define the feasible region F as the intersection of all squares S_i: |x - x_i| + |y - y_i| <= d.
    # We need to check if F intersects with R.
    #
    # The region F can be represented by four linear inequalities derived from the transformation:
    # u = x + y, v = x - y
    # Then |x - x_i| + |y - y_i| = max(|(u - (x_i+y_i))|, |(v - (x_i-y_i))|) ??? No.
    # Actually, |x - x_i| + |y - y_i| = max( (x+y) - (x_i+y_i), (x_i+y_i) - (x+y), (x-y) - (x_i-y_i), (x_i-y_i) - (x-y) )
    # = max( |u - u_i|, |v - v_i| ) where u = x+y, v = x-y, u_i = x_i+y_i, v_i = x_i-y_i.
    # So the condition is max(|u - u_i|, |v - v_i|) <= d.
    # This means |u - u_i| <= d AND |v - v_i| <= d.
    # So for each i: u_i - d <= u <= u_i + d AND v_i - d <= v <= v_i + d.
    #
    # Thus, the feasible region in (u, v) space is a rectangle:
    # u in [max(u_i) - d, min(u_i) + d]
    # v in [max(v_i) - d, min(v_i) + d]
    # Let U_min = max(x_i + y_i) - d, U_max = min(x_i + y_i) + d
    # Let V_min = max(x_i - y_i) - d, V_max = min(x_i - y_i) + d
    #
    # If U_min > U_max or V_min > V_max, then F is empty -> impossible.
    #
    # Now we need to check if the rectangle R (in x,y) intersects with F (in u,v).
    # R is defined by: min_x_opt <= x <= max_x_opt, min_y_opt <= y <= max_y_opt.
    # Transform R to (u, v) space:
    # u = x + y, v = x - y.
    # The range of u in R is [min_x_opt + min_y_opt, max_x_opt + max_y_opt].
    # The range of v in R is [min_x_opt - max_y_opt, max_x_opt - min_y_opt].
    # Let R_u_min = min_x_opt + min_y_opt, R_u_max = max_x_opt + max_y_opt
    # Let R_v_min = min_x_opt - max_y_opt, R_v_max = max_x_opt - min_y_opt
    #
    # Intersection exists if:
    # max(R_u_min, U_min) <= min(R_u_max, U_max) AND
    # max(R_v_min, V_min) <= min(R_v_max, V_max)
    #
    # If intersection exists, then there is a point in R satisfying the d constraint.
    # The minimal total distance is min_total.
    # Otherwise, impossible.

    # Compute bounds for F
    max_u_i = -float('inf')
    min_u_i = float('inf')
    max_v_i = -float('inf')
    min_v_i = float('inf')

    for x, y in zip(xs, ys):
        u = x + y
        v = x - y
        if u > max_u_i: max_u_i = u
        if u < min_u_i: min_u_i = u
        if v > max_v_i: max_v_i = v
        if v < min_v_i: min_v_i = v

    U_min = max_u_i - d
    U_max = min_u_i + d
    V_min = max_v_i - d
    V_max = min_v_i + d

    if U_min > U_max or V_min > V_max:
        print("impossible")
        return

    # Compute bounds for R in (u, v) space
    R_u_min = min_x_opt + min_y_opt
    R_u_max = max_x_opt + max_y_opt
    R_v_min = min_x_opt - max_y_opt
    R_v_max = max_x_opt - min_y_opt

    # Check intersection
    if max(R_u_min, U_min) <= min(R_u_max, U_max) and max(R_v_min, V_min) <= min(R_v_max, V_max):
        print(min_total)
    else:
        print("impossible")

if __name__ == "__main__":
    solve()