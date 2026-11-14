import sys

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    if n == 0:
        print("possible")
        return

    # Precompute prefix balances
    # bal[i] = balance after processing s[0:i]
    # We use 0-based indexing for string, so bal[i] corresponds to prefix of length i
    bal = [0] * (n + 1)
    for i in range(n):
        bal[i+1] = bal[i] + (1 if s[i] == '(' else -1)

    # Check if original is valid
    def is_valid(b):
        mn = 0
        for x in b:
            if x < mn:
                return False
            mn = x
        return mn == 0

    if is_valid(bal):
        print("possible")
        return

    # Try all segments [l, r] (0-based inclusive)
    # Inverting segment [l, r] means flipping signs of bal[l+1]...bal[r+1] relative to bal[l]
    # Actually, the balance at index k (after k chars) changes if k > l.
    # Specifically, for k in [l+1, r+1], the new balance = bal[l] - (bal[k] - bal[l])
    # For k > r+1, the new balance = bal[l] - (bal[r+1] - bal[l]) + (bal[k] - bal[r+1])
    # But simpler: we can simulate the effect on the balance array.
    
    # Let's define a function to check validity after inverting [l, r]
    # We need to check:
    # 1. Prefixes before l: bal[0]...bal[l] must be >= 0 (unchanged)
    # 2. Prefixes inside [l+1, r+1]: new_bal[k] = bal[l] - (bal[k] - bal[l]) = 2*bal[l] - bal[k] must be >= 0
    # 3. Prefixes after r+1: new_bal[k] = bal[l] - (bal[r+1] - bal[l]) + (bal[k] - bal[r+1])
    #    = bal[k] - 2*(bal[r+1] - bal[l]) must be >= 0
    # 4. Final balance must be 0: new_bal[n] = bal[n] - 2*(bal[r+1] - bal[l]) = 0

    # Pre-check: total balance must be even and we must be able to fix it
    # Actually, condition 4 gives us: bal[n] - 2*(bal[r+1] - bal[l]) = 0
    # => bal[r+1] - bal[l] = bal[n] / 2
    # So (bal[n] must be even) and we need to find l, r such that bal[r+1] - bal[l] = bal[n]/2
    
    total_bal = bal[n]
    if total_bal % 2 != 0:
        print("impossible")
        return
    
    target_diff = total_bal // 2
    
    # We need bal[r+1] - bal[l] = target_diff
    # And we need to check the non-negativity conditions for all k.
    
    # To optimize, we can iterate l from 0 to n-1, and for each l, find r such that bal[r+1] = bal[l] + target_diff
    # Then check the three conditions.
    
    # Condition 1: min(bal[0]...bal[l]) >= 0
    # Condition 2: for k in [l+1, r+1], 2*bal[l] - bal[k] >= 0  => bal[k] <= 2*bal[l]
    # Condition 3: for k in [r+1, n], bal[k] - 2*(bal[r+1] - bal[l]) >= 0
    #            Since bal[r+1] - bal[l] = target_diff, this becomes bal[k] - 2*target_diff >= 0
    
    # Precompute prefix minimums for condition 1 and 3
    # min_bal[i] = min(bal[0], ..., bal[i])
    min_bal = [0] * (n + 1)
    cur = 0
    for i in range(n + 1):
        if i == 0:
            min_bal[i] = 0
        else:
            min_bal[i] = min(min_bal[i-1], bal[i])
    
    # For condition 3, we need min(bal[r+1]...bal[n]) >= 2*target_diff
    # Let's precompute suffix minimums
    suf_min = [0] * (n + 2)
    cur = float('inf')
    for i in range(n, -1, -1):
        cur = min(cur, bal[i])
        suf_min[i] = cur
    
    # Now iterate l from 0 to n-1
    # We need r+1 such that bal[r+1] = bal[l] + target_diff
    # r+1 can range from l+1 to n (since r >= l, r+1 >= l+1)
    
    # Create a map from balance value to list of indices where it occurs
    # But since n is up to 5000, we can just iterate r+1 for each l, but that's O(n^2) which is acceptable.
    # However, we can optimize by storing positions of each balance value.
    
    from collections import defaultdict
    pos = defaultdict(list)
    for i in range(n + 1):
        pos[bal[i]].append(i)
    
    # We need to check for each l, if there exists r+1 in pos[bal[l] + target_diff] such that:
    # 1. r+1 >= l+1
    # 2. min_bal[l] >= 0
    # 3. min(bal[l+1]...bal[r+1]) <= 2*bal[l]  (actually we need max(bal[l+1]...bal[r+1]) <= 2*bal[l])
    #    Wait, condition 2: 2*bal[l] - bal[k] >= 0 for all k in [l+1, r+1]
    #    => bal[k] <= 2*bal[l] for all k in [l+1, r+1]
    #    So we need max(bal[l+1]...bal[r+1]) <= 2*bal[l]
    # 4. suf_min[r+1] >= 2*target_diff
    
    # Precompute max in ranges? We can do it on the fly or precompute.
    # Since we iterate l and then r, we can maintain the max as we extend r.
    # But we are jumping to specific r values. Let's just iterate all pairs if n=5000? 
    # 5000^2 = 25e6, which might be tight in Python but let's try to optimize.
    
    # Better approach:
    # For a fixed l, we need r+1 such that:
    #   bal[r+1] = bal[l] + target_diff
    #   r+1 >= l+1
    #   max(bal[l+1]...bal[r+1]) <= 2*bal[l]
    #   suf_min[r+1] >= 2*target_diff
    #   min_bal[l] >= 0
    
    # We can iterate l from 0 to n-1.
    # If min_bal[l] < 0, skip.
    # Then look for r+1 in pos[bal[l] + target_diff] that are >= l+1.
    # For each such r+1, check the other conditions.
    # To check max(bal[l+1]...bal[r+1]) efficiently, we can precompute a 2D structure or just iterate.
    # Given constraints, let's try a slightly optimized O(n^2) worst case but with early breaks.
    
    # Actually, we can iterate r+1 from l+1 to n, and maintain the max balance in [l+1, r+1].
    # But we only care about r+1 where bal[r+1] = bal[l] + target_diff.
    # So for each l, we can iterate through the list of positions for the target balance.
    
    for l in range(n):
        if min_bal[l] < 0:
            continue
        
        val_l = bal[l]
        target = val_l + target_diff
        
        if target not in pos:
            continue
        
        # Get all positions of target balance
        candidates = pos[target]
        # Filter candidates >= l+1
        # Since candidates are sorted, we can use bisect or just iterate
        for r1 in candidates:
            if r1 < l + 1:
                continue
            
            # Check condition 3: suf_min[r1] >= 2*target_diff
            if suf_min[r1] < 2 * target_diff:
                continue
            
            # Check condition 2: max(bal[l+1]...bal[r1]) <= 2*val_l
            # We need to compute max in range [l+1, r1]
            # Since we are iterating, we can do a linear scan, but that makes it O(n^3) worst case.
            # However, note that for a fixed l, as r1 increases, the max is non-decreasing.
            # But we are jumping to specific r1 values.
            # Let's precompute a sparse table or use a segment tree? That might be overkill.
            # Alternatively, since n=5000, O(n^2) total is acceptable if the inner loop is fast.
            # The inner loop here iterates over candidates. In worst case, all positions are candidates, so O(n) per l, total O(n^2).
            # But inside we do a max query which is O(r1-l) = O(n), leading to O(n^3).
            # We need to optimize the max query.
            
            # Precompute max for all ranges? No, too much memory/time.
            # Instead, we can precompute an array max_bal[i][j] but that's O(n^2) space and time.
            # Actually, we can do this: for each l, we iterate r1 from l+1 to n, and maintain current_max.
            # But we only check r1 where bal[r1] == target.
            # So:
            #   current_max = -inf
            #   for k from l+1 to n:
            #       current_max = max(current_max, bal[k])
            #       if bal[k] == target:
            #           check conditions
            # This is O(n) per l, total O(n^2).
            
            # Let's restructure the loop to avoid nested candidate iteration.
            pass
    
    # Restructure to O(n^2)
    for l in range(n):
        if min_bal[l] < 0:
            continue
        
        val_l = bal[l]
        target = val_l + target_diff
        
        # We need to find r1 in [l+1, n] such that bal[r1] == target
        # and check the conditions.
        # We can iterate k from l+1 to n, maintaining max_bal in [l+1, k]
        # and when bal[k] == target, check the rest.
        
        current_max = -10**9
        found = False
        for k in range(l + 1, n + 1):
            if bal[k] > current_max:
                current_max = bal[k]
            
            if bal[k] == target:
                # Check condition 3
                if suf_min[k] >= 2 * target_diff:
                    # Check condition 2
                    if current_max <= 2 * val_l:
                        # All conditions satisfied
                        print("possible")
                        return
    
    print("impossible")

if __name__ == "__main__":
    solve()