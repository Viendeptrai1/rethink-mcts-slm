import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        p = [0] * (n + 1)
        for i in range(1, n + 1):
            p[i] = int(next(iterator))
    except StopIteration:
        return

    visited = [False] * (n + 1)
    q = [0] * (n + 1)

    for i in range(1, n + 1):
        if visited[i]:
            continue

        # Trace the cycle in p starting from i
        cycle = []
        curr = i
        while not visited[curr]:
            visited[curr] = True
            cycle.append(curr)
            curr = p[curr]

        length = len(cycle)
        if length % 2 == 0:
            # Even length cycle: must be split into two interleaved cycles of length length/2
            half = length // 2
            if half == 0:
                # Should not happen for length >= 1
                print("-1")
                return

            # Construct two cycles:
            # Cycle 1: cycle[0], cycle[2], cycle[4], ...
            # Cycle 2: cycle[1], cycle[3], cycle[5], ...
            # In q, these two cycles will map to each other such that q^2 gives the original even cycle.
            
            # Let's build the mapping for q
            # We need q[cycle[2k]] = cycle[2k+1] and q[cycle[2k+1]] = cycle[2k+2] (with wrap around logic)
            # Actually, the standard construction for an even cycle (c0, c1, c2, ..., c_{2m-1}) in p
            # is to set q as two cycles: (c0, c2, c4, ..., c_{2m-2}, c1, c3, ..., c_{2m-1})? 
            # No, that's not quite right.
            # Correct construction:
            # Let the even cycle in p be: c0 -> c1 -> c2 -> ... -> c_{2m-1} -> c0
            # We want q such that q^2 = p.
            # We can form two cycles in q:
            # A: c0 -> c2 -> c4 -> ... -> c_{2m-2} -> c1 -> c3 -> ... -> c_{2m-1} -> c0 ?? No.
            # Let's try a specific example: p = [2, 3, 4, 5, 1, 6] (cycle 1->2->3->4->5->6->1, length 6)
            # We want q such that q^2 = p.
            # One solution: q = [3, 4, 5, 6, 1, 2] (cycle 1->3->5->1 and 2->4->6->2)
            # Check: q[q[1]] = q[3] = 5 != 2. Wait, indices are 1-based.
            # p: 1->2, 2->3, 3->4, 4->5, 5->6, 6->1.
            # q: 1->3, 3->5, 5->1 (cycle 1-3-5) and 2->4, 4->6, 6->2 (cycle 2-4-6).
            # q^2: 1->5, 5->1, 3->1? No.
            # Let's re-evaluate.
            # If q has cycles C1 and C2 of same length L, and they are "interleaved", then q^2 merges them into one cycle of length 2L.
            # Specifically, if C1 = (a0, a1, ..., a_{L-1}) and C2 = (b0, b1, ..., b_{L-1}),
            # and we define q such that q(a_i) = a_{i+1} and q(b_i) = b_{i+1}, then q^2(a_i) = a_{i+2}.
            # This doesn't merge them.
            # The correct way to get a single cycle of length 2L from two cycles of length L in q is:
            # q(a_i) = b_i and q(b_i) = a_{i+1} (indices mod L).
            # Then q^2(a_i) = q(b_i) = a_{i+1}. So q^2 on the set {a} acts as a shift by 1.
            # And q^2(b_i) = q(a_{i+1}) = b_{i+1}. So q^2 on the set {b} acts as a shift by 1.
            # This results in two cycles in q^2, not one.
            
            # Let's try the other way:
            # We have a cycle in p: c0 -> c1 -> c2 -> ... -> c_{2m-1} -> c0.
            # We want to split this into two cycles in q.
            # Let q(c_{2k}) = c_{2k+1} and q(c_{2k+1}) = c_{2k+2} (indices mod 2m).
            # Then q^2(c_{2k}) = c_{2k+2} and q^2(c_{2k+1}) = c_{2k+3}.
            # This means q^2 maps c_i to c_{i+2}.
            # The cycle of q^2 starting at c0 is c0 -> c2 -> c4 -> ... -> c_{2m-2} -> c0 (if 2m is even, this is a cycle of length m).
            # And c1 -> c3 -> ... -> c_{2m-1} -> c1 (another cycle of length m).
            # This gives TWO cycles in q^2, but we only have ONE cycle in p.
            # So this construction is for splitting a cycle in q into two in q^2. We need the reverse.
            
            # Reverse: Given a cycle in p of length 2m, we need to form q such that q^2 is this cycle.
            # This is possible if and only if the cycle length is even? No, wait.
            # If q has a cycle of length L, q^2 has a cycle of length L / gcd(L, 2).
            # If L is odd, gcd(L, 2) = 1, so q^2 has a cycle of length L.
            # If L is even, gcd(L, 2) = 2, so q^2 has two cycles of length L/2.
            # Therefore, a cycle of length 2m in p can come from:
            # 1. A cycle of length 2m in q (if 2m is odd? Impossible since 2m is even).
            # 2. Two cycles of length 2m in q? No.
            # Let's re-read the property.
            # If q has a cycle of length L:
            #   - If L is odd, q^2 has one cycle of length L.
            #   - If L is even, q^2 has two cycles of length L/2.
            # So, if p has a cycle of length K:
            #   - If K is odd, it must come from a cycle of length K in q (since K is odd, it can't come from an even cycle in q which would split into two).
            #   - If K is even, it must come from two cycles of length K in q? No.
            #     If q has a cycle of length 2K (even), q^2 splits it into two cycles of length K.
            #     So if p has a cycle of length K (even), it could be part of a split from a cycle of length 2K in q.
            #     But p has only ONE cycle of length K. If q had a cycle of length 2K, q^2 would produce TWO cycles of length K.
            #     Since p has only one cycle of length K, we cannot have come from a single cycle of length 2K in q.
            #     Could it come from two separate cycles in q?
            #     If q has two cycles of length K, q^2 will have two cycles of length K (if K is odd) or four cycles of length K/2 (if K is even).
            #     This doesn't seem to match "one cycle of length K" in p.
            
            # Wait, I might be confusing the direction.
            # Let's test with the example: p = [2, 1, 4, 3] (n=4).
            # Cycles in p: (1 2) and (3 4). Two cycles of length 2.
            # Output q = [3, 4, 2, 1].
            # q cycles: 1->3->2->1 (length 3)? No.
            # q[1]=3, q[3]=2, q[2]=4, q[4]=1.
            # Cycle: 1->3->2->4->1. Length 4.
            # q^2: 1->2, 2->4, 4->3, 3->1?
            # q[1]=3, q[3]=2 => q^2[1]=2.
            # q[2]=4, q[4]=1 => q^2[2]=1.
            # q[3]=2, q[2]=4 => q^2[3]=4.
            # q[4]=1, q[1]=3 => q^2[4]=3.
            # So q^2 = [2, 1, 4, 3]. Correct.
            # Here, p has two cycles of length 2: (1 2) and (3 4).
            # q has one cycle of length 4: (1 3 2 4).
            # So, two cycles of length K in p (where K is even) can be merged into one cycle of length 2K in q.
            # Condition: We need pairs of cycles of the same even length in p to merge them into a larger cycle in q.
            # If we have an odd number of cycles of a certain even length, we can't pair them all up -> impossible.
            # What about odd length cycles in p?
            # If p has a cycle of odd length K, it must come from a cycle of length K in q (since K is odd, a cycle of length K in q stays length K in q^2).
            # So odd length cycles in p are always solvable (just copy the cycle structure).
            # Even length cycles in p:
            #   - If we have a cycle of length K (even) in p, it must be paired with another cycle of length K in p to form a cycle of length 2K in q.
            #   - If we have an unpaired cycle of even length, it's impossible.
            
            # Algorithm refinement:
            # 1. Decompose p into disjoint cycles.
            # 2. Group cycles by length.
            # 3. For each length L:
            #    - If L is odd:
            #      - Each cycle of length L in p corresponds to a cycle of length L in q.
            #      - Construct q by simply shifting elements in the cycle.
            #    - If L is even:
            #      - We need cycles of length L in p to come in pairs.
            #      - If count[L] is odd, return -1.
            #      - If count[L] is even, pair them up. For each pair of cycles C1 and C2 of length L:
            #        - Construct a cycle of length 2L in q that interleaves C1 and C2.
            #        - How to interleave?
            #          Let C1 = [a0, a1, ..., a_{L-1}] and C2 = [b0, b1, ..., b_{L-1}].
            #          We want q^2 to map a_i -> a_{i+1} and b_i -> b_{i+1} (indices mod L).
            #          And q^2 to map the whole set {a} U {b} as a single cycle of length 2L?
            #          No, q^2 on the set {a} U {b} should produce two cycles of length L (C1 and C2).
            #          Wait, the problem is: given p (which has C1 and C2), find q.
            #          So q^2 must map a_i -> a_{i+1} and b_i -> b_{i+1}.
            #          We need to define q such that q^2(a_i) = a_{i+1} and q^2(b_i) = b_{i+1}.
            #          And q must form a single cycle of length 2L involving all elements of C1 and C2.
            #          Let's try: q(a_i) = b_i and q(b_i) = a_{i+1}.
            #          Then q^2(a_i) = q(b_i) = a_{i+1}. Correct.
            #          Then q^2(b_i) = q(a_{i+1}) = b_{i+1}. Correct.
            #          Does this form a single cycle?
            #          Start at a0: a0 -> b0 -> a1 -> b1 -> a2 -> ... -> a_{L-1} -> b_{L-1} -> a0.
            #          Yes, it forms a single cycle of length 2L.
            #          So the construction is:
            #          For a pair of cycles C1 and C2 of length L:
            #          q[a_i] = b_i
            #          q[b_i] = a_{(i+1) % L}
            
            # Implementation details:
            # - Store cycles in a list of lists.
            # - Use a dictionary to group cycles by length.
            # - Iterate through lengths.
            # - Handle odd lengths: direct mapping.
            # - Handle even lengths: check count, pair up, construct interleaved cycle.

        # Re-implementing the logic inside the loop
        if length % 2 == 1:
            # Odd length: direct mapping
            # Cycle: c0 -> c1 -> c2 -> ... -> c_{L-1} -> c0
            # We want q^2(c_i) = c_{i+1}
            # Set q(c_i) = c_{i + L//2}? No.
            # If q is a cycle of length L, q^2 shifts by 2.
            # We want q^2 to shift by 1.
            # So q should shift by k such that 2k = 1 mod L.
            # Since L is odd, 2 has an inverse mod L.
            # k = (L+1)//2.
            # Example L=3: k = 2. q shifts by 2. q^2 shifts by 4 = 1 mod 3. Correct.
            # Example L=5: k = 3. q shifts by 3. q^2 shifts by 6 = 1 mod 5. Correct.
            
            step = (length + 1) // 2
            for idx in range(length):
                u = cycle[idx]
                v = cycle[(idx + step) % length]
                q[u] = v
        else:
            # Even length: need to pair with another cycle of same length
            # We will handle pairing outside the loop to avoid complexity here
            # Mark this cycle as needing a partner
            pass

    # Let's restart the logic with a cleaner structure
    # Reset q and visited
    q = [0] * (n + 1)
    visited = [False] * (n + 1)
    cycles_by_len = {}

    # Collect cycles
    for i in range(1, n + 1):
        if visited[i]:
            continue
        cycle = []
        curr = i
        while not visited[curr]:
            visited[curr] = True
            cycle.append(curr)
            curr = p[curr]
        
        length = len(cycle)
        if length not in cycles_by_len:
            cycles_by_len[length] = []
        cycles_by_len[length].append(cycle)

    # Process cycles
    for length, cycles in cycles_by_len.items():
        if length % 2 == 1:
            # Odd length: each cycle is independent
            for cycle in cycles:
                step = (length + 1) // 2
                for idx in range(length):
                    u = cycle[idx]
                    v = cycle[(idx + step) % length]
                    q[u] = v
        else:
            # Even length: must be paired
            if len(cycles) % 2 != 0:
                print("-1")
                return
            
            # Pair them up
            for i in range(0, len(cycles), 2):
                c1 = cycles[i]
                c2 = cycles[i+1]
                L = length
                
                # Interleave c1 and c2
                # q[c1[j]] = c2[j]
                # q[c2[j]] = c1[(j+1)%L]
                for j in range(L):
                    u = c1[j]
                    v = c2[j]
                    q[u] = v
                    q[v] = c1[(j + 1) % L]

    # Output result
    print(*(q[1:]))

if __name__ == "__main__":
    solve()