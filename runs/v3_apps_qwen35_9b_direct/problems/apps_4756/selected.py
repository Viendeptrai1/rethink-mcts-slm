import sys
import math

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

    # The distance from point (x, y) to line y = x + a is |x - y + a| / sqrt(2).
    # Unusefulness = (distance)^2 = (x - y + a)^2 / 2.
    # Total unusefulness = sum((x_i - y_i + a)^2) / 2.
    # To minimize sum((x_i - y_i + a)^2), we need to find a that minimizes sum((d_i + a)^2)
    # where d_i = x_i - y_i.
    # This is a standard least squares problem. The optimal a is the mean of (-d_i).
    # Let d_i = x_i - y_i. We want to minimize sum((d_i + a)^2).
    # Derivative w.r.t a: 2 * sum((d_i + a)) = 0 => sum(d_i) + n*a = 0 => a = -mean(d_i).
    
    sum_d = 0.0
    for x, y in points:
        sum_d += (x - y)
    
    a = -sum_d / n
    
    print(f"{a:.6f}")

if __name__ == "__main__":
    solve()