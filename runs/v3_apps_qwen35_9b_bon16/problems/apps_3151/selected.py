import sys
import math

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        n = int(line)
    except ValueError:
        return

    if n <= 0:
        print("impossible")
        return

    # We need m^2 - k^2 = n => (m-k)(m+k) = n
    # Let a = m-k, b = m+k, then a*b = n and b > a (since k >= 0)
    # Also, adding: a + b = 2m => a and b must have the same parity (both even or both odd)
    # Subtracting: b - a = 2k => k = (b - a) / 2

    # Iterate over factors a of n such that a <= sqrt(n)
    limit = int(math.isqrt(n))
    for a in range(1, limit + 1):
        if n % a == 0:
            b = n // a
            # Check parity: (a + b) must be even
            if (a + b) % 2 == 0:
                # Calculate m and k
                m = (a + b) // 2
                k = (b - a) // 2
                # Ensure k >= 0 (guaranteed since b >= a) and m > k (guaranteed since a >= 1)
                # Also ensure we don't have k=0 unless n is a perfect square (which is allowed as long as building is larger)
                # The problem says "surrounding building" implying k < m, which is true here if a >= 1.
                # However, if k=0, it means pool size is 0, which might not be a "pool". 
                # But mathematically n = m^2 - 0 = m^2 is valid per equation.
                # The problem statement says "both the swimming pool and the surrounding building are perfect squares".
                # A side length of 0 is a degenerate square. Usually in such problems k > 0 is implied for a pool to exist.
                # Let's check if k=0 is acceptable. Sample 1: 7 -> 4,3 (k=3). 
                # If input is 4, could be 2,0? Or maybe impossible if pool must be >0.
                # Re-reading: "swimming pool ... are perfect squares". Usually implies non-zero area.
                # If k=0, area is 0. Let's assume k must be >= 1.
                if k == 0:
                    continue
                print(f"{m} {k}")
                return

    print("impossible")

if __name__ == "__main__":
    solve()