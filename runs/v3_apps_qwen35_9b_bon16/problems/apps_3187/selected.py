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

    xs.sort()
    ys.sort()

    median_x = xs[n // 2]
    median_y = ys[n // 2]

    min_dist_x = sum(abs(x - median_x) for x in xs)
    min_dist_y = sum(abs(y - median_y) for y in ys)
    total_min = min_dist_x + min_dist_y

    if total_min > 2 * d:
        # Even the optimal unconstrained point violates the constraint
        # However, we must check if ANY point within d of everyone exists.
        # The set of valid x coordinates is [max_x - d, min_x + d]
        # The set of valid y coordinates is [max_y - d, min_y + d]
        # These intervals must be non-empty and their intersection with the "median" logic must allow a solution.
        # Actually, the condition for existence is:
        # max(xs) - min(xs) <= 2*d AND max(ys) - min(ys) <= 2*d
        # Because any point x must be within d of all xs, so x >= max(xs)-d and x <= min(xs)+d.
        # Such an x exists iff max(xs)-d <= min(xs)+d => max(xs)-min(xs) <= 2d.
        # Same for y.
        # If either dimension fails, impossible.
        print("impossible")
        return

    # If valid region exists, we need to find a point (x, y) in the valid rectangular region
    # that minimizes sum(|xi - x|) + sum(|yi - y|).
    # The function f(x) = sum(|xi - x|) is convex and minimized at any median.
    # Within the valid interval [Lx, Rx], the minimum is at:
    #   - the median if it lies in [Lx, Rx]
    #   - Lx if median < Lx
    #   - Rx if median > Rx
    # Same for y.
    # Then total distance is f(x_opt) + f(y_opt).

    min_x = xs[0]
    max_x = xs[-1]
    Lx = max_x - d
    Rx = min_x + d

    min_y = ys[0]
    max_y = ys[-1]
    Ly = max_y - d
    Ry = min_y + d

    # The valid region is [Lx, Rx] x [Ly, Ry]
    # We know Lx <= Rx and Ly <= Ry from the check above.

    def get_best_1d(coords, L, R):
        # coords is sorted
        m = coords[len(coords) // 2]
        if L <= m <= R:
            return m
        elif m < L:
            return L
        else:
            return R

    best_x = get_best_1d(xs, Lx, Rx)
    best_y = get_best_1d(ys, Ly, Ry)

    total_dist = sum(abs(x - best_x) for x in xs) + sum(abs(y - best_y) for y in ys)
    print(total_dist)

if __name__ == "__main__":
    solve()