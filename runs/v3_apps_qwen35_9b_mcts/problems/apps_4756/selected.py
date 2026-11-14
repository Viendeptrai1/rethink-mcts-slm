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

    xs = []
    ys = []
    for _ in range(n):
        xs.append(int(next(iterator)))
        ys.append(int(next(iterator)))

    # We need to minimize sum((x_i - y_i - a)^2)
    # Let d_i = x_i - y_i
    # The function is sum((d_i - a)^2)
    # The minimum occurs at a = mean(d_i)
    
    # Calculate sum of d_i
    sum_d = 0.0
    for i in range(n):
        sum_d += (xs[i] - ys[i])
    
    a = sum_d / n
    
    # Ensure that if a is effectively zero, it prints as 0.000000 instead of -0.000000
    if abs(a) < 1e-9:
        a = 0.0
    
    print(f"{a:.6f}")

if __name__ == "__main__":
    solve()