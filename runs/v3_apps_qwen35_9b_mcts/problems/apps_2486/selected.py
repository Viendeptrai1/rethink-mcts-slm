import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    K = int(data[1])
    A = []
    for i in range(N):
        A.append(int(data[2 + i]))
    
    total_sum = sum(A)
    
    if total_sum < K:
        print(N)
        return
    
    # Precompute prefix and suffix reachable sums using bitsets (integers)
    # prefix[i] represents the set of reachable sums using cards 0..i-1
    # suffix[i] represents the set of reachable sums using cards i..N-1
    
    prefix = [1] * (N + 1)
    suffix = [1] * (N + 1)
    
    # Compute prefix DP
    for i in range(N):
        val = A[i]
        # Shift left by val and OR with current
        prefix[i+1] = prefix[i] | (prefix[i] << val)
        
        # Optimization: mask to keep only bits up to K (actually we need up to K, but for correctness of ">= K" logic later, 
        # we technically need sums up to K. However, if a sum exceeds K, it's still "good". 
        # To save space/time, we can cap at K, but shifting beyond K is fine as long as we check correctly.
        # Actually, for the condition "sum >= K - a_i", we need to know if there exists a sum S in the other cards such that S >= K - a_i.
        # If we cap the bitset at K, we lose information about sums > K. But any sum > K is equivalent to K for the purpose of being "good".
        # However, the condition is specifically: is there a subset of OTHER cards with sum S such that S + a_i >= K?
        # This is equivalent to S >= K - a_i.
        # So we need to know if any bit from (K - a_i) upwards is set.
        # If we cap the bitset at K, we might miss that a sum of K+5 exists, but K+5 >= K - a_i is true anyway.
        # The only issue is if K - a_i > K, which is impossible since a_i >= 1.
        # So capping at K is safe? 
        # Wait: if we have a sum S = K + 100, and we need S >= K - a_i. Since K+100 >= K - a_i is always true, 
        # having a bit set at K is sufficient to say "yes" for any threshold <= K.
        # But we need to be careful: the bitset represents exact sums. 
        # If we mask with (1 << (K+1)) - 1, we lose sums > K. 
        # But do we need sums > K? 
        # The condition is: exists S in others such that S >= K - a_i.
        # If there is a sum S > K, then S >= K - a_i is definitely true (since a_i >= 1 => K - a_i < K).
        # So if we have ANY sum >= K - a_i, we are good.
        # If we cap our bitset at K, we know all sums in [0, K]. 
        # If the bit at (K - a_i) or higher is set in the capped bitset, we are good.
        # What if the only sums >= K - a_i are all > K? 
        # Example: K=10, a_i=1. Need S >= 9. 
        # Suppose other cards can only form sum 12. 
        # If we cap at 10, we see sum 10 is reachable? No, 12 is not 10.
        # If we cap, we lose the fact that 12 exists. 
        # But 12 >= 9 is true. 
        # The problem is: does the capped bitset tell us if there is a sum >= 9?
        # If we cap at 10, we have bits 0..10. If 12 exists, we don't have a bit for 12. 
        # We might have a bit for 10? Not necessarily.
        # So capping at K is NOT safe if the only valid sums are > K.
        # However, note that if a sum S > K exists, then S is "good" on its own. 
        # But we are checking subsets of OTHER cards. 
        # If the sum of ALL other cards is < K - a_i, then no subset works.
        # If the sum of ALL other cards >= K - a_i, does it mean there is a subset with sum >= K - a_i?
        # Not necessarily! We need a subset sum, not just the total sum.
        # But wait: if the total sum of others is >= K - a_i, is there a subset with sum >= K - a_i?
        # Yes, the set of all others itself is a subset with sum = total_sum_others.
        # So if total_sum_others >= K - a_i, then the answer is YES.
        # Therefore, we don't need to know if specific sums > K exist, we only need to know if the total sum of others is >= K - a_i?
        # NO! The definition of "good" is sum >= K.
        # The condition for card i being unnecessary:
        # "If, for any good subset of the cards containing card i, the set that can be obtained by eliminating card i from the subset is also good"
        # Let S be a good subset containing i. So sum(S) >= K.
        # Let S' = S \ {i}. We need sum(S') >= K.
        # This must hold for ALL good subsets S containing i.
        # Equivalently: There does NOT exist a good subset S containing i such that sum(S \ {i}) < K.
        # sum(S \ {i}) = sum(S) - a_i.
        # So we need: For all S containing i with sum(S) >= K, we have sum(S) - a_i >= K.
        # This is equivalent to: There is NO subset S' of OTHER cards such that:
        #   sum(S') + a_i >= K  AND  sum(S') < K.
        # In other words, there is NO subset of other cards with sum in [K - a_i, K - 1].
        # So card i is unnecessary IF AND ONLY IF there is NO subset of other cards with sum in [K - a_i, K - 1].
        # This is equivalent to: All subset sums of other cards are either < K - a_i OR >= K.
        # So we need to check if the range [K - a_i, K - 1] contains any reachable sum from other cards.
        
        # Therefore, we DO need to know the exact reachable sums up to K-1.
        # Sums >= K in the "other" cards don't matter for the "bad" condition because if sum(S') >= K, then it's not in the bad range.
        # The bad range is [K - a_i, K - 1].
        # So we only need to track reachable sums up to K-1.
        # If a sum >= K is formed by other cards, we can cap it at K (or ignore it) because it's not in the bad range.
        # Actually, if we cap at K, then any sum >= K becomes K. 
        # Then we check if K is in [K - a_i, K - 1]? No, K is not in that range.
        # So capping at K is safe. We just need to know if any bit in [K - a_i, K - 1] is set.
        # If we cap at K, the bit at K represents "sum >= K".
        # The bits 0 to K-1 represent exact sums.
        # So we can mask with (1 << K) - 1 to keep 0..K-1, and separately track if sum >= K is possible?
        # Actually, simpler: we only care about bits 0 to K-1.
        # If a sum >= K is formed, it doesn't help us find a sum in [K - a_i, K - 1] unless we break it down, which we can't.
        # But wait: if the total sum of others is huge, but no subset sum falls in [K - a_i, K - 1], then card i is unnecessary.
        # So we only need to know the reachable sums in the range [0, K-1].
        # Any sum >= K can be ignored for the purpose of checking the interval [K - a_i, K - 1].
        # So we can mask the bitset to keep only bits 0 to K-1.
        # But wait: what if the only way to get a sum >= K - a_i is via a sum >= K?
        # Then that sum is not in [K - a_i, K - 1], so it's not a "bad" sum.
        # The condition for "NOT unnecessary" is: exists S' (subset of others) such that K - a_i <= sum(S') <= K - 1.
        # So we only need to check if any bit in [K - a_i, K - 1] is set in the bitset of other cards.
        # So we can maintain bitsets capped at K (i.e., bits 0 to K-1).
        # If a sum >= K is formed, we can just set the bit at K-1? No, that would be wrong.
        # Better: we only care about bits 0 to K-1. We can mask with (1 << K) - 1.
        # But if the total sum of others is >= K, does that imply there is a subset sum in [K - a_i, K - 1]?
        # Not necessarily. Example: K=10, a_i=1. Bad range [9, 9].
        # Others: {10}. Sum=10. Subset sums: {0, 10}. 
        # Is 9 in {0, 10}? No. So card i is unnecessary.
        # If we cap at 10 (bits 0..9), we see {0}. 9 is not set. Correct.
        # Example: K=10, a_i=2. Bad range [8, 9].
        # Others: {5, 5}. Sums: 0, 5, 10.
        # 8, 9 not present. Card i unnecessary.
        # Capped bitset (0..9): {0, 5}. Correct.
        # Example: K=10, a_i=2. Bad range [8, 9].
        # Others: {8}. Sums: 0, 8.
        # 8 is present. Card i is NOT unnecessary.
        # Capped bitset: {0, 8}. Correct.
        # So yes, we only need to track sums in [0, K-1].
        # We can mask with (1 << K) - 1.
        
        # Let's re-verify the logic:
        # Card i is unnecessary <=> NO subset of others has sum in [K - a_i, K - 1].
        # So we compute reachable sums of others, but we only care about sums < K.
        # If a sum >= K is reachable, it is not in [K - a_i, K - 1] (since K - a_i <= K - 1).
        # So we can safely ignore sums >= K.
        # Thus, we maintain bitsets of size K (bits 0 to K-1).
        
        pass

    # Recompute with masking
    prefix = [1] * (N + 1)
    suffix = [1] * (N + 1)
    
    # Mask for bits 0 to K-1
    mask = (1 << K) - 1
    
    for i in range(N):
        val = A[i]
        prefix[i+1] = (prefix[i] | (prefix[i] << val)) & mask
        
    for i in range(N-1, -1, -1):
        val = A[i]
        suffix[i] = (suffix[i+1] | (suffix[i+1] << val)) & mask
        
    unnecessary_count = 0
    
    for i in range(N):
        # Check if there is any subset of others with sum in [K - A[i], K - 1]
        # Others: prefix[i] U suffix[i+1]
        # Combine: prefix[i] | suffix[i+1]
        others = prefix[i] | suffix[i+1]
        
        # We need to check if any bit from (K - A[i]) to (K - 1) is set.
        # Range start: L = K - A[i]
        # If L < 0, then the range starts at 0? 
        # But A[i] >= 1, so K - A[i] <= K - 1.
        # If K - A[i] < 0, then the lower bound is negative, but sums are non-negative.
        # So effective lower bound is max(0, K - A[i]).
        # However, if K - A[i] <= 0, then the range [K - A[i], K - 1] includes [0, K - 1].
        # Since 0 is always reachable (empty set), if K - A[i] <= 0, then 0 is in the range, so there exists a bad subset (empty set).
        # Wait: if K - A[i] <= 0, then A[i] >= K.
        # If A[i] >= K, then the card itself is good.
        # Consider a good subset S containing i. Since A[i] >= K, S is good.
        # S' = S \ {i}. sum(S') = sum(S) - A[i].
        # We need sum(S') >= K for i to be unnecessary.
        # But if S = {i}, sum(S) = A[i] >= K. S' = empty, sum(S') = 0.
        # Is 0 >= K? No (since K >= 1).
        # So if A[i] >= K, then the subset {i} is good, but removing i gives empty set (sum 0 < K).
        # So card i is NOT unnecessary.
        # Our logic: bad range [K - A[i], K - 1].
        # If A[i] >= K, then K - A[i] <= 0.
        # The range is [<=0, K-1]. Since sums are >= 0, this is [0, K-1].
        # Is 0 in the reachable sums of others? Yes (empty set).
        # So there exists a bad subset (empty set). So card i is NOT unnecessary.
        # This matches.
        
        L = K - A[i]
        if L < 0:
            L = 0
        
        # Check if any bit in [L, K-1] is set in 'others'
        # Create a mask for [L, K-1]
        if L >= K:
            # Range is empty or above K-1
            # But L = K - A[i]. Since A[i] >= 1, L <= K-1.
            # So L >= K is impossible unless A[i] <= 0, but A[i] >= 1.
            # So this case won't happen.
            has_bad = False
        else:
            # Mask for bits L to K-1
            # (1 << K) - 1 is all 1s from 0 to K-1.
            # (1 << L) - 1 is all 1s from 0 to L-1.
            # So (1 << K) - (1 << L) is 1s from L to K-1.
            range_mask = ((1 << K) - 1) ^ ((1 << L) - 1)
            if (others & range_mask) != 0:
                has_bad = True
            else:
                has_bad = False
        
        if not has_bad:
            unnecessary_count += 1
            
    print(unnecessary_count)

if __name__ == '__main__':
    solve()