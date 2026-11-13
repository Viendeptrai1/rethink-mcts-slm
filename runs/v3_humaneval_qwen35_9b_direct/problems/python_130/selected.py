def tri(n):
    if n == 0:
        return [1]
    
    # Initialize the sequence with known values
    # tri(1) = 3
    # tri(2) = 1 + 2/2 = 2
    # tri(4) = 3 (Wait, let's re-verify the pattern based on the problem statement)
    
    # The problem states:
    # tri(1) = 3
    # tri(n) = 1 + n/2 if n is even
    # tri(n) = tri(n-1) + tri(n-2) + tri(n+1) if n is odd
    
    # There is a logical issue in the recurrence for odd n because it depends on tri(n+1)
    # which is a future value. This suggests the recurrence might be misstated or requires
    # a different interpretation. Let's look at the example:
    # tri(3) = tri(2) + tri(1) + tri(4) = 2 + 3 + 3 = 8
    # Here tri(4) is used to calculate tri(3). But tri(4) is defined as 1 + 4/2 = 3.
    # So for odd n, we need tri(n+1). Since n+1 is even, we can calculate it directly.
    
    # Let's build the sequence iteratively.
    # We need to compute up to index n.
    # Base cases:
    # index 0: The problem doesn't explicitly define tri(0), but the example tri(3) returns [1, 3, 2, 8].
    # The list has n+1 elements. For n=3, indices are 0, 1, 2, 3.
    # Values: tri(0)=1, tri(1)=3, tri(2)=2, tri(3)=8.
    # So tri(0) = 1 is implied.
    
    result = [1, 3]  # tri(0) and tri(1)
    
    # If n=0, return [1]
    if n == 0:
        return [1]
    if n == 1:
        return [1, 3]
    
    # Calculate tri(2)
    # n=2 is even: 1 + 2/2 = 2
    result.append(2)
    
    # Now we have [1, 3, 2] for indices 0, 1, 2.
    # We need to go up to index n.
    # For odd i, tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
    # But tri(i+1) is even, so tri(i+1) = 1 + (i+1)/2.
    # So for odd i, tri(i) = tri(i-1) + tri(i-2) + (1 + (i+1)/2)
    
    # Let's verify for i=3:
    # tri(3) = tri(2) + tri(1) + (1 + 4/2) = 2 + 3 + 3 = 8. Correct.
    
    # We can compute iteratively.
    # We have result[0], result[1], result[2].
    # Next is i=3 (odd).
    # Then i=4 (even) -> 1 + 4/2 = 3.
    # Then i=5 (odd) -> tri(4) + tri(3) + tri(6).
    # tri(6) = 1 + 6/2 = 4.
    
    # Algorithm:
    # Maintain the list `result`.
    # Loop i from 2 to n.
    # If i is even: append 1 + i/2.
    # If i is odd: calculate using the formula involving i+1.
    
    # However, the formula for odd i uses tri(i+1).
    # tri(i+1) is even, so it's 1 + (i+1)/2.
    # So we don't need to store future values, just calculate the even term on the fly.
    
    for i in range(3, n + 1):
        if i % 2 == 0:
            val = 1 + i // 2
            result.append(val)
        else:
            # i is odd
            # tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
            # tri(i+1) = 1 + (i+1)/2
            next_even_val = 1 + (i + 1) // 2
            val = result[i-1] + result[i-2] + next_even_val
            result.append(val)
            
    return result