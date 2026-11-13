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

    b = []
    for _ in range(n):
        b.append(int(next(iterator)))

    a = [0] * n

    # We have the system:
    # a[i] + a[i-1] = b[i]   (indices mod n)
    # Let's define a[0] as x.
    # Then a[1] = b[0] - a[0] = b[0] - x
    # a[2] = b[1] - a[1] = b[1] - (b[0] - x) = b[1] - b[0] + x
    # In general: a[i] = x + (-1)^i * (b[0] - b[1] + b[2] - ... +/- b[i-1])
    # More precisely, we can express a[i] in terms of x and the known b values.
    #
    # Let's derive the recurrence:
    # a[i] = b[i-1] - a[i-1]
    #
    # Expanding:
    # a[0] = x
    # a[1] = b[0] - x
    # a[2] = b[1] - (b[0] - x) = b[1] - b[0] + x
    # a[3] = b[2] - (b[1] - b[0] + x) = b[2] - b[1] + b[0] - x
    #
    # Pattern:
    # a[i] = x * (-1)^i + C[i]
    # where C[i] is a constant derived from b.
    #
    # Specifically:
    # C[0] = 0
    # C[1] = -b[0]
    # C[2] = b[1] - b[0]
    # C[3] = -b[2] + b[1] - b[0]
    #
    # General formula for C[i]:
    # C[i] = sum_{j=0}^{i-1} (-1)^(i-1-j) * b[j]
    #
    # Now use the ring closure condition: a[n-1] + a[n-2] = b[n-1]
    # Actually, the condition is that the sequence wraps around correctly.
    # The relation a[i] + a[i-1] = b[i] must hold for i=0 as well (with a[-1] being a[n-1]).
    # So: a[0] + a[n-1] = b[0]
    #
    # Substitute a[0] = x and a[n-1] = x * (-1)^(n-1) + C[n-1]
    # x + x * (-1)^(n-1) + C[n-1] = b[0]
    # x * (1 + (-1)^(n-1)) = b[0] - C[n-1]
    #
    # Case 1: n is odd.
    # (-1)^(n-1) = 1.
    # x * (1 + 1) = 2x = b[0] - C[n-1]
    # x = (b[0] - C[n-1]) / 2
    # Since a solution exists and numbers are integers, this division will be exact.
    #
    # Case 2: n is even.
    # (-1)^(n-1) = -1.
    # x * (1 - 1) = 0 = b[0] - C[n-1]
    # This implies b[0] must equal C[n-1]. If the input is valid, this holds.
    # In this case, x can be any value such that all a[i] >= 0.
    # We need to find the smallest non-negative x (or any valid x) that makes all a[i] >= 0.
    #
    # Let's compute C array first.
    # C[0] = 0
    # C[i] = b[i-1] - C[i-1] * (-1) ? Let's re-verify recurrence.
    # a[i] = b[i-1] - a[i-1]
    # a[i] = b[i-1] - (x*(-1)^(i-1) + C[i-1])
    # a[i] = -x*(-1)^(i-1) + b[i-1] - C[i-1]
    # a[i] = x*(-1)^i + (b[i-1] - C[i-1])
    # So C[i] = b[i-1] - C[i-1]
    #
    # Base case:
    # i=0: a[0] = x. So C[0] = 0.
    # i=1: C[1] = b[0] - C[0] = b[0]. Wait, earlier I said C[1] = -b[0]. Let's re-check signs.
    #
    # Re-derivation carefully:
    # a[0] = x
    # a[1] = b[0] - a[0] = b[0] - x = -x + b[0]
    # a[2] = b[1] - a[1] = b[1] - (b[0] - x) = x + (b[1] - b[0])
    # a[3] = b[2] - a[2] = b[2] - (x + b[1] - b[0]) = -x + (b[2] - b[1] + b[0])
    #
    # Coefficients of x:
    # i=0: +1
    # i=1: -1
    # i=2: +1
    # i=3: -1
    # So coeff is (-1)^i. Correct.
    #
    # Constant part C[i]:
    # C[0] = 0
    # C[1] = b[0]
    # C[2] = b[1] - b[0]
    # C[3] = b[2] - b[1] + b[0]
    #
    # Recurrence for C:
    # C[i] = b[i-1] - C[i-1]
    # Check:
    # C[1] = b[0] - 0 = b[0]. Correct.
    # C[2] = b[1] - b[0]. Correct.
    # C[3] = b[2] - (b[1] - b[0]) = b[2] - b[1] + b[0]. Correct.
    #
    # So algorithm:
    # 1. Compute C array of size n.
    # 2. If n is odd:
    #    x = (b[0] - C[n-1]) // 2
    # 3. If n is even:
    #    The equation 0 = b[0] - C[n-1] must hold. If not, input invalid (but problem says valid).
    #    We need to choose x such that a[i] = x*(-1)^i + C[i] >= 0 for all i.
    #    For even i: x + C[i] >= 0 => x >= -C[i]
    #    For odd i: -x + C[i] >= 0 => x <= C[i]
    #    So we need max(-C[i] for even i) <= x <= min(C[i] for odd i).
    #    Since a solution exists, such an x exists. We can pick the smallest non-negative x,
    #    which is max(0, max(-C[i] for even i)).
    #    However, we must also satisfy x <= min(C[i] for odd i).
    #    Let's just compute the range and pick a valid x. To be safe and simple, we can pick the lower bound.
    #    Lower bound L = max(0, max(-C[i] for i even))
    #    Check if L <= min(C[i] for i odd). If yes, x = L.
    #    If not, try L+1? But problem guarantees solution.
    #    Actually, let's just find the tightest lower bound and verify.
    #    Wait, if n is even, the system is underdetermined (0=0). Any x in the range works.
    #    We want non-negative a[i].
    #    Constraints:
    #      For even i: x >= -C[i]
    #      For odd i: x <= C[i]
    #    So x_min = max(0, max(-C[i] for i in 0..n-1 if i%2==0))
    #    x_max = min(C[i] for i in 0..n-1 if i%2==1)
    #    We know x_min <= x_max. We can output x_min.

    c = [0] * n
    current_c = 0
    for i in range(1, n):
        current_c = b[i-1] - current_c
        c[i] = current_c

    if n % 2 == 1:
        # Odd case
        # x = (b[0] - c[n-1]) / 2
        numerator = b[0] - c[n-1]
        x = numerator // 2
    else:
        # Even case
        # Determine range for x
        # x >= -c[i] for even i
        # x <= c[i] for odd i
        # Also x >= 0
        
        min_x = 0
        for i in range(0, n, 2):
            if -c[i] > min_x:
                min_x = -c[i]
        
        # We assume a solution exists, so min_x will be <= max possible x.
        # Let's just use min_x.
        x = min_x

    # Construct the result
    result = []
    for i in range(n):
        if i % 2 == 0:
            val = x + c[i]
        else:
            val = -x + c[i]
        result.append(val)

    # Output
    for val in result:
        print(val)

if __name__ == "__main__":
    solve()