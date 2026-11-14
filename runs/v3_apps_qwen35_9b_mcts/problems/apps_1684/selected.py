import sys

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    segments = []
    for _ in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        # Normalize segment so that start < end for easier comparison
        if u > v:
            u, v = v, u
        segments.append((u, v))

    # We need to find if there exists a rotation k (1 <= k < n) such that the set of segments is invariant.
    # A rotation by k units maps point i to (i + k - 1) % n + 1.
    # Instead of checking every k, we can check only divisors of n.
    # Why? If a pattern repeats every k steps, then k must divide n for the pattern to close perfectly on the circle of size n.
    # Actually, the period k doesn't strictly have to be a divisor of n in the sense of generating the whole group, 
    # but if the configuration is invariant under rotation by k, then it is also invariant under rotation by gcd(k, n).
    # Let g = gcd(k, n). The rotation by g is also a symmetry. And g must be a divisor of n.
    # So we only need to check rotations by d where d is a divisor of n and d > 0.
    # The rotation amount is d. We rotate each point i by d.
    # New position of u: (u - 1 + d) % n + 1.
    
    # Precompute divisors of n
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i*i != n:
                divisors.append(n // i)
    
    divisors.sort()
    
    # Remove 1 because k must be >= 1, but if k=1 works, then any divisor works? 
    # Wait, the problem asks if there exists ANY k in [1, n-1].
    # If k=1 works, then the whole circle is symmetric.
    # Our divisor list includes 1. If we find a divisor d > 0 such that rotation by d works, we output Yes.
    # Note: d=0 is not allowed (k < n), but d=n is equivalent to d=0, so we skip n.
    # We check divisors d where 1 <= d < n.
    
    # Optimization: Convert segments to a canonical representation for fast lookup?
    # Since n and m are up to 10^5 and 2*10^5, O(m * number_of_divisors) might be too slow if number_of_divisors is large.
    # However, the maximum number of divisors for n <= 100,000 is 128 (for 75600).
    # 128 * 200,000 = 25.6 million operations, which is acceptable in Python if implemented efficiently.
    
    # Let's represent the set of segments as a set of tuples.
    seg_set = set(segments)
    
    # Check each divisor d from 1 to n-1
    for d in divisors:
        if d == n:
            continue
        
        # Check rotation by d
        # We need to verify that for every segment (u, v) in seg_set, 
        # the rotated segment (u', v') is also in seg_set.
        # Since the set is finite, we can just generate all rotated segments and compare sets.
        
        # Generate rotated segments
        rotated_segments = []
        for u, v in segments:
            # Rotate u and v by d clockwise
            # Points are 1-based. Convert to 0-based for modulo arithmetic.
            u0 = u - 1
            v0 = v - 1
            u_new = (u0 + d) % n + 1
            v_new = (v0 + d) % n + 1
            
            if u_new > v_new:
                u_new, v_new = v_new, u_new
            rotated_segments.append((u_new, v_new))
        
        # Check if the set of rotated segments is identical to the original set
        if set(rotated_segments) == seg_set:
            print("Yes")
            return

    print("No")

if __name__ == "__main__":
    solve()