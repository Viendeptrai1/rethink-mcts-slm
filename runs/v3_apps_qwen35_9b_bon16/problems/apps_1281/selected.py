import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))

    a = []
    for _ in range(n):
        a.append(int(next(iterator)))

    # Prefix XOR array
    # p[i] = a[0] ^ ... ^ a[i-1], p[0] = 0
    # The XOR of segment [l, r] (1-based) is p[r] ^ p[l-1]
    # We want p[r] ^ p[l-1] != 0 for as many pairs (l, r) with l <= r as possible.
    # This is equivalent to counting pairs (i, j) with 0 <= i < j <= n such that p[i] != p[j].
    # Total pairs = n*(n+1)//2.
    # Pairs with p[i] == p[j] are the "bad" ones. We want to minimize bad pairs.
    # Since we can flip any a[i], we can effectively choose whether p[i] and p[i-1] are related by XOR with mask = (2^k - 1).
    # Actually, flipping a[i] changes the relation between p[i] and p[i-1].
    # Specifically, if we don't flip, p[i] = p[i-1] ^ a[i].
    # If we flip, p[i] = p[i-1] ^ a[i] ^ mask, where mask = 2^k - 1.
    # So for each step i (from 1 to n), we can choose the value of p[i] to be either:
    #   val1 = p[i-1] ^ a[i]
    #   val2 = p[i-1] ^ a[i] ^ mask
    # Note that val1 ^ val2 = mask.
    # We need to construct a sequence p[0], p[1], ..., p[n] such that p[0]=0, and for each i,
    # p[i] is either p[i-1]^a[i] or p[i-1]^a[i]^mask.
    # We want to minimize the number of pairs (i, j) with p[i] == p[j].
    # This is equivalent to: for each distinct value v, minimize (count[v] * (count[v]-1)) / 2.
    # Since the total number of pairs is fixed, minimizing sum(count_v choose 2) is equivalent to making the distribution of values as uniform as possible?
    # Actually, the function f(x) = x(x-1)/2 is convex. To minimize sum f(count_v), we want the counts to be as equal as possible.
    # However, the values are not arbitrary. The sequence is constrained.
    # Let's analyze the constraints.
    # p[i] is determined by the choices c_1, c_2, ..., c_n where c_i in {0, 1}.
    # p[i] = (prefix_xor_original up to i) ^ (mask if sum(c_1...c_i) is odd else 0).
    # Let S_i be the prefix sum of choices (mod 2). Then p[i] = P[i] ^ (S_i * mask), where P[i] is the prefix XOR of original array.
    # We have p[0] = 0 (since P[0]=0, S_0=0).
    # The sequence of P[i] is fixed. The sequence of S_i can be any sequence starting with S_0=0 and changing by 0 or 1 at each step.
    # Actually, S_i can be any sequence of bits s_0, s_1, ..., s_n with s_0=0.
    # Wait, the choice is: at step i, we choose whether to flip a[i] or not.
    # If we flip, it contributes to the cumulative XOR mask.
    # Let x_i be 0 if we don't flip a[i], 1 if we flip.
    # Then p[i] = P[i] ^ ( (x_1 + ... + x_i) % 2 ) * mask.
    # Let s_i = (x_1 + ... + x_i) % 2. s_0 = 0.
    # s_i can be 0 or 1. And s_i depends on s_{i-1} and x_i. Since x_i can be 0 or 1, s_i can be either s_{i-1} or 1-s_{i-1}.
    # So s_i can be any sequence of bits starting with 0? Yes, because at each step we can choose to keep the parity or flip it.
    # Wait, if s_{i-1}=0, we can choose x_i=0 -> s_i=0, or x_i=1 -> s_i=1.
    # If s_{i-1}=1, we can choose x_i=0 -> s_i=1, or x_i=1 -> s_i=0.
    # So indeed, s_i can be ANY sequence of bits with s_0=0.
    # This means we can choose the value of the "mask offset" for each prefix independently?
    # No, the constraint is just s_0=0. s_i can be 0 or 1 freely for i>=1.
    # So for each i from 1 to n, we can choose s_i independently to be 0 or 1?
    # Yes. Because to set s_i = b, if s_{i-1} was a, we just pick x_i such that a ^ x_i = b. Since x_i can be 0 or 1, this is always possible.
    # So we have complete freedom to assign s_1, s_2, ..., s_n to be 0 or 1.
    # Then p[i] = P[i] if s_i=0, and p[i] = P[i] ^ mask if s_i=1.
    # We want to assign s_1, ..., s_n in {0, 1} to minimize the number of pairs (i, j) with p[i] == p[j].
    # Note p[0] is fixed to 0 (s_0=0).
    # Let V_0 = 0.
    # For each i in 1..n, we have two choices for p[i]:
    #   Option 0: val = P[i]
    #   Option 1: val = P[i] ^ mask
    # Let's call these two potential values for index i as u_i and v_i.
    # Notice that u_i ^ v_i = mask.
    # Also, for any i, j, if we choose Option A for i and Option B for j, we get a collision if the resulting values are equal.
    # We want to select a sequence of choices to minimize collisions.
    # This looks like a dynamic programming problem or a flow problem, but n is 200,000.
    # However, notice that the values only take two forms relative to the fixed P array.
    # Actually, let's group the indices by the value of P[i].
    # Suppose P[i] = X. Then the two options are X and X^mask.
    # Suppose P[j] = Y. Options are Y and Y^mask.
    # Collisions happen if:
    #   1. We chose X for i and X for j (i.e., both chose the "no mask" option relative to their P).
    #      This requires P[i] == P[j] and both chose 0.
    #   2. We chose X^mask for i and Y^mask for j.
    #      This requires P[i]^mask == P[j]^mask => P[i] == P[j] and both chose 1.
    #   3. We chose X for i and Y^mask for j.
    #      Requires P[i] == P[j]^mask => P[j] == P[i]^mask. One chose 0, one chose 1.
    #   4. We chose X^mask for i and Y for j.
    #      Requires P[i]^mask == P[j] => P[j] == P[i]^mask. One chose 1, one chose 0.
    #
    # Let's rephrase.
    # We have a set of indices I_0 = {i | P[i] is some value X}.
    # And a set of indices I_1 = {i | P[i] = X^mask}.
    # Note that if P[i] = X, then P[i]^mask = X^mask.
    # So the universe of values involved in collisions is pairs of values (X, X^mask).
    # Let's group indices based on the pair {P[i], P[i]^mask}.
    # Since X and X^mask form a pair, and applying ^mask swaps them, the pairs are disjoint.
    # Let's iterate over all unique values of P[i]. But wait, P[i] can be up to 2^30.
    # We only care about P[i] that actually appear.
    # Let's count frequencies of each P[i].
    # Map: val -> count.
    # The pairs are {v, v^mask}.
    # Let's consider a pair of values {A, B} where B = A^mask.
    # Suppose in our array, we have:
    #   cntA = number of i such that P[i] == A
    #   cntB = number of i such that P[i] == B
    # (If A == B, i.e., mask=0, but mask = 2^k-1 >= 1, so A != B unless k=0 which is not allowed).
    # For each index i with P[i] == A, we can choose p[i] = A (state 0) or p[i] = A^mask = B (state 1).
    # For each index j with P[j] == B, we can choose p[j] = B (state 0) or p[j] = B^mask = A (state 1).
    # Let x_i be the choice for i in the first group (0 -> A, 1 -> B).
    # Let y_j be the choice for j in the second group (0 -> B, 1 -> A).
    # We want to minimize collisions.
    # Collisions occur between:
    #   - Two indices from group A both choosing A (x_i=0, x_j=0).
    #   - Two indices from group A both choosing B (x_i=1, x_j=1).
    #   - Two indices from group B both choosing B (y_j=0, y_k=0).
    #   - Two indices from group B both choosing A (y_j=1, y_k=1).
    #   - One from A choosing A (x_i=0) and one from B choosing A (y_j=1). -> Collision at A.
    #   - One from A choosing B (x_i=1) and one from B choosing B (y_j=0). -> Collision at B.
    #
    # Let's denote:
    #   Let u be the number of indices from group A that choose A (x=0).
    #   Then (cntA - u) indices from group A choose B.
    #   Let v be the number of indices from group B that choose B (y=0).
    #   Then (cntB - v) indices from group B choose A.
    #
    # Collisions:
    #   At value A: u + (cntB - v) elements. Pairs: (u + cntB - v) * (u + cntB - v - 1) / 2.
    #   At value B: (cntA - u) + v elements. Pairs: (cntA - u + v) * (cntA - u + v - 1) / 2.
    #
    # We want to minimize this sum over u in [0, cntA] and v in [0, cntB].
    # Let S_A = u + cntB - v
    # Let S_B = cntA - u + v
    # Note that S_A + S_B = cntA + cntB = Total count in this pair of values. This is constant.
    # Let T = cntA + cntB.
    # We want to minimize f(S_A) + f(T - S_A) where f(x) = x(x-1)/2.
    # Since f is convex, the sum is minimized when S_A and T - S_A are as close as possible.
    # i.e., S_A should be floor(T/2) or ceil(T/2).
    # Can we achieve any S_A?
    # S_A = u - v + cntB.
    # Range of u: [0, cntA]. Range of v: [0, cntB].
    # Min S_A = 0 - cntB + cntB = 0.
    # Max S_A = cntA - 0 + cntB = cntA + cntB = T.
    # Since u and v can vary independently and cover a range, can we hit every integer in [0, T]?
    # S_A = u - v + cntB.
    # We can set u from 0 to cntA. For a fixed u, v can be from 0 to cntB.
    # So S_A ranges from u - cntB + cntB = u to u + cntB.
    # The union of [u, u + cntB] for u in [0, cntA] is [0, cntA + cntB] = [0, T].
    # Yes, we can achieve any integer S_A from 0 to T.
    # So for each pair {A, A^mask}, we simply distribute the total count T as evenly as possible between the two resulting values.
    # The minimum collisions for this pair is:
    #   let c1 = T // 2
    #   let c2 = T - c1
    #   cost = c1*(c1-1)//2 + c2*(c2-1)//2
    #
    # But wait, what about collisions within the same group if A and B are not the same pair?
    # Collisions only happen if the resulting values are equal.
    # If we pick value V for an index i, and value V for index j, they collide.
    # The possible values we can generate are { P[i] ^ (s_i * mask) }.
    # If P[i] and P[j] belong to different pairs {X, X^mask} and {Y, Y^mask}, can they collide?
    # Suppose P[i] = X, P[j] = Y.
    # Result for i: X or X^mask.
    # Result for j: Y or Y^mask.
    # Collision if X = Y (same pair), X = Y^mask (same pair), X^mask = Y (same pair), X^mask = Y^mask (same pair).
    # So collisions only occur between indices whose P values belong to the same pair {Z, Z^mask}.
    # Therefore, the groups {A, A^mask} are independent.
    #
    # Algorithm:
    # 1. Compute prefix XORs P[0]...P[n]. P[0]=0.
    # 2. Count frequencies of each P[i]. Use a hash map.
    # 3. Iterate through the map. For each unique value X:
    #      If we haven't processed X^mask yet, process the pair {X, X^mask}.
    #      Let cntX = count[X], cntY = count[X^mask].
    #      T = cntX + cntY.
    #      Add (T//2)*(T//2 - 1)//2 + (T - T//2)*(T - T//2 - 1)//2 to total_bad_pairs.
    #      Mark both X and X^mask as processed.
    # 4. Answer = Total_pairs - total_bad_pairs.
    #    Total_pairs = n * (n + 1) // 2.
    
    # Implementation details:
    # n up to 200,000. O(n) or O(n log n) is fine. Hash map is O(n) average.
    # Be careful with large integers in Python (automatic support).
    # k up to 30, so numbers fit in standard 64-bit int, Python handles arbitrarily large anyway.

    mask = (1 << k) - 1
    prefix_xor = 0
    counts = {}
    
    # Include P[0] = 0
    counts[0] = 1
    
    for x in a:
        prefix_xor ^= x
        if prefix_xor in counts:
            counts[prefix_xor] += 1
        else:
            counts[prefix_xor] = 1
            
    total_pairs = n * (n + 1) // 2
    bad_pairs = 0
    processed = set()
    
    for val, count in counts.items():
        if val in processed:
            continue
        pair_val = val ^ mask
        if pair_val in processed:
            continue
            
        # Process the pair {val, pair_val}
        # But wait, if val == pair_val? 
        # val = val ^ mask => mask = 0. Since k >= 1, mask >= 1. So val != pair_val always.
        
        cnt1 = counts.get(val, 0)
        cnt2 = counts.get(pair_val, 0)
        
        t = cnt1 + cnt2
        c1 = t // 2
        c2 = t - c1
        bad_pairs += (c1 * (c1 - 1)) // 2
        bad_pairs += (c2 * (c2 - 1)) // 2
        
        processed.add(val)
        processed.add(pair_val)
        
    print(total_pairs - bad_pairs)

if __name__ == '__main__':
    solve()