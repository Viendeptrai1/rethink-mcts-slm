import sys
from math import gcd

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
        # Normalize segment so that start < end
        if u > v:
            u, v = v, u
        segments.append((u, v))

    # If there are no segments, it's trivially symmetric for any rotation, but m >= 1 per constraints.
    # We need to find if there exists a k (1 <= k < n) such that rotating by k maps the set of segments to itself.
    # The rotation amount k must be a divisor of n? Not necessarily, but the minimal rotation angle that preserves symmetry
    # must divide the full circle. If a rotation by k works, then rotating by k repeatedly will generate a subgroup.
    # The smallest such k (generator of the symmetry group) must divide n.
    # So we only need to check k where k is a divisor of n and k < n.
    
    # Let's represent the set of segments as a canonical signature that is invariant under rotation shifts.
    # However, checking all divisors is efficient enough since sum of divisors is small compared to n for large n.
    # But n up to 100,000, checking all divisors is fine.
    
    # Alternative approach:
    # Create a boolean array or hash set of segments.
    # For each divisor d of n (where d < n), check if rotating every segment by d results in a segment present in the original set.
    # If for any d this holds, output Yes.
    # If no such d exists, output No.
    
    # Wait, the problem says "is there an integer k". It doesn't require k to be a divisor, but if a rotation by k works,
    # then the order of this rotation divides n. Let g = gcd(k, n). The effective rotation is g.
    # So we only need to check k = g where g divides n and g < n.
    
    # Let's collect unique segments in a set for O(1) lookup.
    seg_set = set()
    for u, v in segments:
        seg_set.add((u, v))
    
    # Find all divisors of n
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    
    # Filter divisors: we need k such that 1 <= k < n.
    # The effective rotation step is the gcd of the rotation amount and n.
    # So checking all proper divisors d of n is sufficient.
    
    possible = False
    for d in divisors:
        if d == n:
            continue
        
        # Check rotation by d
        # For each segment (u, v), the rotated segment should be ((u+d-1)%n + 1, (v+d-1)%n + 1) normalized
        # Actually, points are 1-based.
        # Rotating point p clockwise by d: new_p = (p + d - 1) % n + 1
        valid = True
        for u, v in segments:
            # Normalize u, v to 0-based for easier modulo math
            u0 = u - 1
            v0 = v - 1
            
            u0_rot = (u0 + d) % n
            v0_rot = (v0 + d) % n
            
            u1 = u0_rot + 1
            v1 = v0_rot + 1
            
            # Normalize the rotated segment
            if u1 > v1:
                u1, v1 = v1, u1
            
            if (u1, v1) not in seg_set:
                valid = False
                break
        
        if valid:
            possible = True
            break
    
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()