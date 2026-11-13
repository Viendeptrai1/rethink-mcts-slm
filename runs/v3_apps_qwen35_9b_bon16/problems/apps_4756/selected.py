import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return
    
    points = []
    for _ in range(N):
        x = int(next(iterator))
        y = int(next(iterator))
        points.append((x, y))
    
    # We want to minimize sum_i ( (x_i - y_i - a)^2 ) / 2
    # Let d_i = x_i - y_i
    # Minimize sum (d_i - a)^2
    # The optimal a is the mean of d_i
    sum_d = 0.0
    for x, y in points:
        sum_d += (x - y)
    
    a = sum_d / N
    print(f"{a:.6f}")

if __name__ == "__main__":
    solve()