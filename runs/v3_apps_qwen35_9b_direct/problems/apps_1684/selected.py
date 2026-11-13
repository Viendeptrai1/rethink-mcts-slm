import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    
    segments = []
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        if u > v:
            u, v = v, u
        segments.append((u, v))
    
    # Normalize segments to be relative to point 1 for easier comparison
    # A segment (u, v) can be represented by the set of differences from 1:
    # diff1 = (u - 1) % n, diff2 = (v - 1) % n
    # But since it's a circle, we can also represent it by the arc length between them.
    # However, the simplest way to check rotational symmetry is to check if the set of segments
    # is invariant under rotation by k.
    
    # Let's represent each segment as a sorted tuple of (min_dist, max_dist) where dist is from 1.
    # Actually, let's just store the segments as tuples (min(u,v), max(u,v)) and then check rotations.
    
    # To optimize, we can create a "signature" of the configuration.
    # The configuration is rotationally symmetric if there exists a k such that rotating all segments by k yields the same set.
    # This is equivalent to checking if the set of segments is periodic with period k.
    
    # We can use a polynomial rolling hash or simply check divisors of n.
    # Since n <= 100,000, checking all divisors is feasible.
    
    # First, let's normalize the segments to be relative to 1.
    # For a segment (u, v), the relative positions are (u-1)%n and (v-1)%n.
    # But the segment itself is defined by the two points.
    # If we rotate by k, a segment (u, v) becomes ((u+k-1)%n + 1, (v+k-1)%n + 1).
    
    # Let's create a canonical representation of the set of segments.
    # We can represent the set of segments as a sorted list of tuples.
    # Then we can check if rotating the list by k results in the same list.
    
    # However, a more efficient way is to check if the "pattern" of segments repeats.
    # We can create an array of size n where each index i has a list of segments starting at i.
    # But segments can start at any point.
    
    # Alternative approach:
    # Represent the configuration as a string or list of hashes.
    # For each point i, we can store the set of segments connected to i.
    # But segments are undirected.
    
    # Let's try a different approach:
    # Check all divisors of n. For each divisor d, check if rotating by d works.
    # If rotating by d works, then the image is rotationally symmetric.
    # Note: The problem asks for ANY k (1 <= k < n). If there is a k, then there is a divisor d of k such that rotating by d also works?
    # Not necessarily. But if rotating by k works, then rotating by gcd(k, n) also works.
    # So we only need to check divisors of n.
    
    # Let's verify this:
    # If rotating by k works, then the set of segments S is invariant under rotation by k.
    # This implies S is invariant under rotation by gcd(k, n).
    # So we only need to check divisors of n.
    
    # Steps:
    # 1. Find all divisors of n.
    # 2. For each divisor d, check if rotating by d works.
    # 3. If any d works, output "Yes", else "No".
    
    # To check if rotating by d works:
    # Create a set of segments.
    # For each segment (u, v), compute the rotated segment (u', v') = ((u-1+d)%n + 1, (v-1+d)%n + 1).
    # Normalize the rotated segment (min, max).
    # Check if the set of rotated segments is equal to the original set.
    
    # Optimization:
    # Instead of creating a new set every time, we can use a hash of the set.
    # Or we can sort the segments and compare.
    
    # Given n <= 100,000 and m <= 200,000, sorting takes O(m log m).
    # Number of divisors can be large for highly composite numbers, but for n <= 100,000, the maximum number of divisors is 128 (for 75600).
    # So checking all divisors is feasible.
    
    # Let's implement this.
    
    # Precompute divisors
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    
    # Sort divisors to check smaller ones first (optional)
    divisors.sort()
    
    # Create a canonical representation of the segments
    # We will store segments as tuples (min(u,v), max(u,v))
    # And sort them to create a canonical list.
    
    canonical_segments = []
    for u, v in segments:
        if u > v:
            u, v = v, u
        canonical_segments.append((u, v))
    canonical_segments.sort()
    
    # Convert to a tuple for hashing or just keep as list
    canonical_tuple = tuple(canonical_segments)
    
    # Check each divisor
    for d in divisors:
        if d == n:
            continue # k must be < n
        
        # Check rotation by d
        # We need to check if rotating each segment by d gives the same set of segments.
        # Instead of creating a new set, we can check if the sorted list of rotated segments equals the canonical list.
        
        # But creating a new list of m segments and sorting it takes O(m log m).
        # Total time: O(num_divisors * m log m).
        # With num_divisors <= 128 and m <= 200,000, this might be too slow (128 * 200000 * 18 ~ 4.6e8 operations).
        # We need a faster check.
        
        # Alternative: Use a hash of the set of segments.
        # We can compute a hash of the canonical segments.
        # Then for each divisor, compute the hash of the rotated segments and compare.
        # But computing the hash still requires iterating over all segments.
        # O(num_divisors * m). This is 128 * 200,000 = 2.56e7, which is acceptable.
        
        # Let's use a simple hash: sum of (u * v) for all segments? No, that's not unique.
        # We can use a polynomial hash or a tuple hash.
        # Python's tuple hash is good, but creating a tuple of m elements is O(m).
        # So we can just create a tuple of the rotated segments and compare hashes.
        
        # Actually, we can avoid sorting if we use a set.
        # But creating a set of m elements is O(m).
        # So total time O(num_divisors * m) is acceptable.
        
        # Let's implement the set-based check.
        
        # But wait, creating a set of m elements might be slow due to hashing overhead.
        # Let's try to optimize.
        
        # We can represent the configuration as a list of "events" or use a different approach.
        # Another idea: The configuration is rotationally symmetric if and only if the "pattern" of segments repeats every d.
        # We can create an array of size n where each index i has a list of segments starting at i.
        # But segments are undirected, so a segment (u, v) can be seen as starting at u and ending at v, or vice versa.
        # Let's define a segment as starting at the smaller index and ending at the larger index.
        # Then for each i, we can store the list of segments starting at i.
        # But this doesn't capture the full structure because the segment (u, v) is also connected to v.
        
        # Let's go back to the set-based check but optimize the hash.
        # We can use a rolling hash or a simple sum of hashes.
        # Let's assign a random 64-bit integer to each possible segment (u, v) where 1 <= u < v <= n.
        # Then the hash of the configuration is the sum of these random integers for all segments.
        # If two configurations have the same hash, they are likely the same.
        # But we need to be careful about collisions.
        # We can use multiple hashes or a large random seed.
        
        # However, since we are checking exact equality, we can just use the set of segments.
        # Let's try to implement the set-based check with a simple optimization:
        # Instead of creating a new set, we can check if the rotated segments are in the original set.
        # But we need to check if the sets are equal, not just if the rotated segments are a subset.
        # Since the number of segments is the same, if all rotated segments are in the original set, then the sets are equal.
        
        # So the check is:
        # For each segment (u, v) in the original set, compute the rotated segment (u', v').
        # Check if (u', v') is in the original set.
        # If all are in the set, then the sets are equal.
        
        # This is O(m) per divisor.
        # Total time O(num_divisors * m).
        
        # Let's implement this.
        
        # Precompute the set of segments for fast lookup
        seg_set = set(canonical_segments)
        
        # Check rotation by d
        all_in = True
        for u, v in canonical_segments:
            # Rotate u and v by d
            u_new = (u - 1 + d) % n + 1
            v_new = (v - 1 + d) % n + 1
            if u_new > v_new:
                u_new, v_new = v_new, u_new
            if (u_new, v_new) not in seg_set:
                all_in = False
                break
        
        if all_in:
            print("Yes")
            return
    
    print("No")

if __name__ == "__main__":
    solve()