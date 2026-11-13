def tri(n):
    if n == 0:
        return [1]
    
    result = [1, 3]
    
    if n == 1:
        return result
    
    # We need to compute up to index n
    # We know:
    # tri(1) = 3
    # tri(2) = 1 + 2/2 = 2
    # tri(3) = tri(2) + tri(1) + tri(4) -> but we don't have tri(4) yet
    
    # Let's re-read the problem carefully.
    # The recurrence for odd n is: tri(n) = tri(n-1) + tri(n-2) + tri(n+1)
    # This is unusual because it depends on a future value (n+1).
    # Let's look at the example:
    # tri(3) = tri(2) + tri(1) + tri(4) = 2 + 3 + 3 = 8
    # So tri(4) = 3.
    # How do we get tri(4)?
    # tri(4) is even, so tri(4) = 1 + 4/2 = 3. That matches!
    
    # So the pattern seems to be:
    # For even n: tri(n) = 1 + n/2
    # For odd n: tri(n) = tri(n-1) + tri(n-2) + tri(n+1)
    # But to compute tri(n) for odd n, we need tri(n+1).
    # However, tri(n+1) is even, so we can compute it directly using the even formula!
    # tri(n+1) = 1 + (n+1)/2
    
    # Let's verify with tri(3):
    # tri(3) = tri(2) + tri(1) + tri(4)
    # tri(2) = 1 + 2/2 = 2
    # tri(1) = 3 (base case)
    # tri(4) = 1 + 4/2 = 3
    # tri(3) = 2 + 3 + 3 = 8. Correct.
    
    # So the algorithm is:
    # 1. Start with known values: tri(0)=1, tri(1)=3
    # 2. For i from 2 to n:
    #    - If i is even: tri(i) = 1 + i/2
    #    - If i is odd: tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
    #      where tri(i+1) = 1 + (i+1)/2 (since i+1 is even)
    
    # Wait, the problem says "return a list of the first n + 1 numbers".
    # So we need indices 0 to n.
    # tri(0) is not explicitly defined in the recurrence, but the example tri(3) = [1, 3, 2, 8]
    # suggests tri(0) = 1.
    
    # Let's build the list iteratively.
    # We need to handle the odd case carefully.
    # For an odd index i, we need tri(i+1). Since i+1 is even, we can compute it on the fly.
    
    # Initialize
    sequence = [1, 3]  # tri(0) and tri(1)
    
    if n == 0:
        return [1]
    if n == 1:
        return [1, 3]
    
    # We need to go up to n
    # For i from 2 to n:
    for i in range(2, n + 1):
        if i % 2 == 0:
            # Even index
            val = 1 + i // 2
            sequence.append(val)
        else:
            # Odd index
            # tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
            # tri(i+1) is even, so tri(i+1) = 1 + (i+1)/2
            tri_i_plus_1 = 1 + (i + 1) // 2
            tri_i_minus_1 = sequence[-1]
            tri_i_minus_2 = sequence[-2]
            val = tri_i_minus_1 + tri_i_minus_2 + tri_i_plus_1
            sequence.append(val)
    
    return sequence