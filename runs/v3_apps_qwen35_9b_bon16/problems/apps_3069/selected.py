import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    if n % 2 != 0:
        print("impossible")
        return

    # Precompute prefix balance: bal[i] = balance of s[0:i]
    # balance: '(' adds 1, ')' subtracts 1
    # We need final total balance to be 0.
    
    # We will check all possible segments [l, r] to invert.
    # Instead of simulating each, we use a more efficient check.
    # But given n <= 5000, O(n^2) is acceptable (25e6 operations roughly, might be tight in Python but let's try optimized logic).
    # Actually 5000^2 = 25,000,000. In Python this might TLE if the inner loop is heavy.
    # Let's try to optimize the check.

    # Define balance array
    # Let's map '(' to 1 and ')' to -1
    # We want to find if there exists l, r such that after flipping s[l:r+1], the whole string has balance 0 at all points (and ends at 0).

    # Let original array be a[i] where '(' -> 1, ')' -> -1.
    # Flipping a segment [l, r] changes a[i] to -a[i] for l <= i <= r.
    # New balance at index k (0-based, after k+1 chars) is:
    # If k < l: same as original.
    # If l <= k < r: prefix_sum_original[k+1] - 2 * (prefix_sum_original[l] - prefix_sum_original[l])? No.
    # Let P[i] be prefix sum of original array up to i (P[0]=0).
    # Sum of segment [l, r] (inclusive 0-based indices for string, so l to r) is P[r+1] - P[l].
    # Let this sum be S.
    # If we flip the segment, the new sum of the segment becomes -S.
    # The change in total prefix sum at index k (0-based count of chars processed) depends on whether the interval [l, r] overlaps with [0, k].
    # Specifically, if we consider the prefix sum after k characters (indices 0 to k-1):
    # Case 1: k <= l: No change. New_P[k] = P[k].
    # Case 2: l < k <= r: The segment partially or fully covers. The part from l to k-1 is flipped.
    #   Original contribution of [l, k-1] is P[k] - P[l].
    #   New contribution is -(P[k] - P[l]).
    #   So New_P[k] = P[l] + (-(P[k] - P[l])) = 2*P[l] - P[k].
    # Case 3: k > r: The whole segment [l, r] is flipped.
    #   Original contribution of [l, r] is P[r+1] - P[l].
    #   New contribution is -(P[r+1] - P[l]).
    #   So New_P[k] = P[k] - 2*(P[r+1] - P[l]).

    # Conditions for validity:
    # 1. Final balance New_P[n] == 0.
    # 2. For all k in 1..n, New_P[k] >= 0.

    # Let's precompute P.
    P = [0] * (n + 1)
    for i in range(n):
        val = 1 if s[i] == '(' else -1
        P[i+1] = P[i] + val

    # Condition 1: Final balance must be 0.
    # New_P[n] = P[n] - 2*(P[r+1] - P[l]) = 0
    # => P[r+1] - P[l] = P[n] / 2
    # Let target_segment_sum = P[n] / 2.
    # If P[n] is odd, impossible immediately.
    target = P[n] / 2
    if target != int(target):
        print("impossible")
        return
    target = int(target)

    # We need to find l, r such that:
    # 1. P[r+1] - P[l] == target
    # 2. For all k, New_P[k] >= 0.

    # Let's iterate over l and r. O(n^2).
    # Optimization: For a fixed l, we need P[r+1] = P[l] + target.
    # We can precompute positions of each prefix sum value.
    # However, we also need to check the min prefix condition efficiently.

    # Check conditions for a fixed [l, r]:
    # Min prefix condition:
    # For k in 1..l: min(P[k]) >= 0. (This must hold for original string up to l)
    # For k in l+1..r: min(2*P[l] - P[k]) >= 0 => P[k] <= 2*P[l].
    # For k in r+1..n: min(P[k] - 2*(P[r+1] - P[l])) >= 0 => P[k] >= 2*(P[r+1] - P[l]).
    # Note: P[r+1] - P[l] = target.
    # So for k > r: P[k] >= 2*target.

    # So for a fixed l and r satisfying the sum condition:
    # 1. min(P[1..l]) >= 0
    # 2. max(P[l+1..r]) <= 2*P[l]
    # 3. min(P[r+1..n]) >= 2*target
    # Also implicitly, since we require New_P[k] >= 0 for all k, we must check these ranges.
    # Also note that for k in [1, l], New_P[k] = P[k], so we need min(P[1..l]) >= 0.
    # But wait, if the original string has negative prefix before l, we cannot fix it by flipping [l, r].
    # So if min(P[1..l]) < 0, this l is invalid for any r >= l.

    # Precompute prefix mins and suffix mins.
    # prefix_min[i] = min(P[0]...P[i])? Actually we care about 1..i.
    # Let's define:
    # min_P[i] = min(P[0], P[1], ..., P[i])
    # But condition is for k=1..l, P[k] >= 0. So min(P[1..l]) >= 0.
    # Since P[0]=0, if min(P[0..l]) < 0, it could be P[0] is 0, so min might be 0. But we only care about k>=1.
    # Actually P[0] is always 0. If any P[k] < 0 for k<=l, then invalid.
    # So we need min(P[1..l]) >= 0.
    # Similarly for suffix: min(P[r+1..n]) >= 2*target.

    # Precompute min from right:
    # suff_min[i] = min(P[i], P[i+1], ..., P[n])
    
    suff_min = [0] * (n + 2)
    curr = float('inf')
    for i in range(n, -1, -1):
        if P[i] < curr:
            curr = P[i]
        suff_min[i] = curr

    # Precompute max from left for the range check?
    # We need max(P[l+1..r]) <= 2*P[l].
    # We can precompute max in range? Or just iterate.
    # Since we iterate l and r, and for fixed l, r is determined by P[r+1] = P[l] + target.
    # There might be multiple r's.
    
    # Let's store indices for each prefix sum value.
    from collections import defaultdict
    pos = defaultdict(list)
    for i in range(n + 1):
        pos[P[i]].append(i)

    # Also precompute prefix min check:
    # is_valid_prefix[l] = (min(P[1..l]) >= 0)
    # We can compute this array.
    valid_prefix = [True] * (n + 1)
    current_min = 0 # P[0] is 0, but we check k>=1.
    # Actually we need min(P[1], ..., P[l]) >= 0.
    # Let's track min from 1 to i.
    min_so_far = 0
    # P[0] is 0.
    # For l=0, range 1..0 is empty, condition vacuously true? Yes, l=0 means flip starts at first char.
    # But we need to check k=1..l. If l=0, no k.
    # Let's compute an array min_P_1_to_i where min_P_1_to_i[i] = min(P[1]...P[i]) for i>=1, and 0 for i=0.
    min_p_1 = [0] * (n + 1)
    curr = float('inf')
    for i in range(1, n + 1):
        if P[i] < curr:
            curr = P[i]
        min_p_1[i] = curr
        # Check validity
        if curr < 0:
            valid_prefix[i] = False
        else:
            valid_prefix[i] = True

    # Now iterate l from 0 to n-1 (since r >= l, and r+1 <= n, so l <= n-1)
    # r+1 can go up to n.
    # target = P[r+1] - P[l]
    # We need P[r+1] = P[l] + target.
    
    # To speed up, for each l, we look for r such that P[r+1] == P[l] + target.
    # Then we check the conditions.
    
    found = False
    
    # Optimization: Precompute max in range? 
    # We need max(P[l+1..r]) <= 2*P[l].
    # Since n is 5000, O(n^2) with simple checks might pass if constant factor is small.
    # Let's try O(n^2) with early breaks.

    for l in range(n): # l is 0-based start index of segment. r is 0-based end index.
        # Condition: min(P[1..l]) >= 0. If not, skip.
        if not valid_prefix[l]:
            continue
        
        pl = P[l]
        needed = pl + target
        
        # Find all r such that P[r+1] == needed.
        if needed not in pos:
            continue
        
        for r_plus1 in pos[needed]:
            r = r_plus1 - 1
            if r < l:
                continue
            
            # Check conditions:
            # 1. max(P[l+1..r]) <= 2*pl
            # 2. min(P[r+1..n]) >= 2*target
            
            # Check condition 2 first, might be faster to fail early.
            # min(P[r+1..n]) is suff_min[r+1]
            if suff_min[r+1] < 2 * target:
                continue
            
            # Check condition 1: max(P[l+1..r]) <= 2*pl
            # If l == r, range l+1 to r is empty? 
            # If l=r, we flip one char. The condition "max(P[l+1..r])" is over empty set?
            # The range of k for the second case is l < k <= r.
            # If l=r, there is no k such that l < k <= r. So condition 2 is vacuously true.
            # So if l == r, condition 1 is true.
            if l == r:
                # Just one more check? No, covered.
                found = True
                break
            
            # If l < r, we need to check max.
            # We can compute max on the fly. O(n) per pair, total O(n^3) worst case.
            # We need to optimize this.
            # Precompute range max? RMQ with sparse table? O(n log n) build, O(1) query.
            # Or since we iterate l and specific r's, maybe we can do better.
            # Given constraints and Python, O(n^2) total queries is risky if each is O(n).
            # Let's implement Sparse Table for Range Maximum Query on P array.
            
            # Actually, let's re-evaluate complexity.
            # Number of pairs (l, r) is O(n^2).
            # If we do O(1) check, total O(n^2).
            # Sparse table build O(n log n). Query O(1).
            # This is feasible.

            # Let's break out of inner loops if found.
            # We'll implement RMQ.
            
            # But wait, we are inside a function. Building RMQ inside the loop is bad.
            # Build once outside.
            
            # Let's restructure.

            pass # placeholder to break logic

    # Let's rewrite with RMQ.
    
    # Re-calculate needed logic with RMQ.
    
    # Build Sparse Table for Range Maximum Query on P[1..n]
    # Indices for P are 0..n. We care about ranges [l+1, r].
    # If l+1 > r, max is -infinity (condition holds).
    
    # Log table
    LOG = [0] * (n + 2)
    for i in range(2, n + 2):
        LOG[i] = LOG[i >> 1] + 1
    
    K = LOG[n + 1] + 1
    st = [[0] * (n + 1) for _ in range(K)]
    
    for i in range(n + 1):
        st[0][i] = P[i]
    
    for j in range(1, K):
        length = 1 << j
        for i in range(n + 1 - length + 1):
            st[j][i] = max(st[j-1][i], st[j-1][i + (1 << (j-1))])
    
    def query_max(L, R):
        if L > R:
            return -float('inf')
        j = LOG[R - L + 1]
        return max(st[j][L], st[j][R - (1 << j) + 1])

    found = False
    for l in range(n):
        if not valid_prefix[l]:
            continue
        
        pl = P[l]
        needed = pl + target
        
        if needed not in pos:
            continue
        
        for r_plus1 in pos[needed]:
            r = r_plus1 - 1
            if r < l:
                continue
            
            # Condition 2: min(P[r+1..n]) >= 2*target
            if suff_min[r+1] < 2 * target:
                continue
            
            # Condition 1: max(P[l+1..r]) <= 2*pl
            if l < r:
                mx = query_max(l+1, r)
                if mx > 2 * pl:
                    continue
            
            found = True
            break
        if found:
            break
            
    if found:
        print("possible")
    else:
        print("impossible")

if __name__ == "__main__":
    solve()