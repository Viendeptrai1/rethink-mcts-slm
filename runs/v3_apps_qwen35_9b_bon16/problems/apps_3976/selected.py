import sys
from collections import Counter

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        p = int(next(iterator))
        
        a = [int(next(iterator)) for _ in range(n)]
        b = [int(next(iterator)) for _ in range(m)]
    except StopIteration:
        return

    if m == 0:
        # If b is empty, technically every q satisfies the condition? 
        # But constraints say m >= 1, so this case won't happen per problem statement.
        print(0)
        print()
        return

    # Count frequencies in b
    b_count = Counter(b)
    total_b = sum(b_count.values())

    # We need to check indices q such that we take elements at:
    # q-1, q-1+p, q-1+2p, ..., q-1+(m-1)p (0-based indexing for array a)
    # Let start index i = q - 1. Then i must satisfy:
    # i >= 0
    # i + (m-1)*p < n  => i <= n - 1 - (m-1)*p
    
    max_start = n - 1 - (m - 1) * p
    if max_start < 0:
        print(0)
        print()
        return

    # We only need to consider starting positions i where i % p == r for some remainder r.
    # However, the step is p, so all positions in a valid sequence for a specific q share the same remainder modulo p.
    # Actually, the sequence is fixed by the start index i: i, i+p, i+2p...
    # Different q's correspond to different start indices i.
    # But note: if we shift by p, the sequence of indices shifts by p, which is just the next element in the arithmetic progression.
    # Wait, the problem asks for q such that the sequence b can be obtained from a[q-1], a[q-1+p]... by rearranging.
    # This means we are looking at subsequences of a with step p.
    # Since the step is p, the indices involved are all congruent modulo p.
    # So we can process each remainder class modulo p independently.
    
    # For a fixed remainder r (0 <= r < p), we extract the subsequence:
    # indices: r, r+p, r+2p, ...
    # Let this subsequence be S_r.
    # We need to find how many windows of length m in S_r match the multiset b.
    
    # However, n and m are up to 2*10^5. We cannot do a naive O(m) check for each q.
    # Total number of q is roughly n. O(n*m) is too slow.
    # We need an efficient way to check sliding windows over the subsequences.
    
    # Approach:
    # 1. Group indices of a by i % p.
    # 2. For each group, we have a list of values. Let's call it L.
    # 3. We want to find starting positions in L such that the window of length m matches b_count.
    # 4. This is a standard sliding window with frequency counts.
    #    We maintain a count of matched elements.
    #    Since values can be large (10^9), we use a dictionary or coordinate compression, but dictionary is fine.
    #    Optimization: We only care about elements present in b.
    
    # Let's refine the sliding window on each remainder class.
    # For a list L of length k, we need windows of size m.
    # Number of windows = k - m + 1.
    # We can use a counter for the current window and compare with b_count.
    # To optimize comparison, we can maintain a variable `matches` which counts how many distinct numbers 
    # have count in window == count in b.
    # But since we only care if window == b, we can maintain:
    # - current_window_counts
    # - a variable `ok` indicating if current_window_counts == b_count.
    # However, comparing full counters is O(distinct elements). We need O(1) or O(log) updates.
    
    # Better approach for sliding window equality:
    # Maintain a counter `diff` which tracks the difference between window and target.
    # Actually, simpler: maintain a variable `balanced_count` = number of elements x where window_count[x] == b_count[x].
    # And a variable `total_needed` = number of distinct elements in b.
    # When moving the window:
    #   Remove element `out`:
    #     old_count = window[out]
    #     if old_count == b[out]: balanced_count -= 1
    #     window[out] -= 1
    #     new_count = window[out]
    #     if new_count == b[out]: balanced_count += 1
    #   Add element `in`:
    #     old_count = window[in]
    #     if old_count == b[in]: balanced_count -= 1
    #     window[in] += 1
    #     new_count = window[in]
    #     if new_count == b[in]: balanced_count += 1
    # Check if balanced_count == total_needed AND the window length is correct (which it is by construction).
    # Wait, this logic works if we only track elements that are in b. Elements not in b don't affect the equality 
    # as long as their count in window is 0. But if the window contains an element not in b, then the window != b.
    # So we also need to ensure that no extra elements exist.
    # Actually, if window length is m and b length is m, and for all x in b, window_count[x] == b_count[x], 
    # then the window must be exactly b (since sum of counts is m).
    # So we just need to track elements present in b.
    # We can ignore elements not in b. If we encounter an element not in b, the window is invalid immediately?
    # Yes, because if window has an element not in b, it can't be a permutation of b.
    # So we can optimize: if an element is not in b_count, any window containing it is invalid.
    
    # Algorithm:
    # 1. Precompute b_count.
    # 2. Group indices of a by i % p.
    # 3. For each group:
    #      Extract values: L = [a[i] for i in range(r, n, p)]
    #      If len(L) < m: continue
    #      Initialize window of first m elements.
    #      Calculate initial balance.
    #      Iterate through L with a sliding window of size m.
    #      If balanced, record the starting index in original array a (which is r + window_start * p).
    #      Then slide: remove L[i], add L[i+m].
    
    # Optimization: Instead of storing all groups explicitly which might use O(N) memory (fine),
    # we can iterate r from 0 to p-1.
    # Note: p can be up to 2*10^5, so iterating r from 0 to p-1 is fine.
    # Inside, we iterate through the subsequence. Total work is O(N) because each element of a is visited once per remainder class it belongs to (exactly once).
    
    valid_qs = []
    
    # Precompute b_count
    b_counter = Counter(b)
    b_keys = set(b_counter.keys())
    total_distinct_b = len(b_keys)
    
    # We will collect answers. 
    # Note: q = i + 1 where i is the 0-based start index.
    
    # To avoid creating many lists, we can iterate r and generate the subsequence on the fly or via a generator,
    # but since we need to look ahead (m steps), we might as well extract the subsequence.
    # Given N=2e5, extracting is fine.
    
    for r in range(p):
        # Extract subsequence starting at r with step p
        # Indices: r, r+p, r+2p, ...
        # We can use slicing with step if we construct the list of indices, but slicing the array 'a' directly is not possible with step unless we copy.
        # Creating a list for each remainder is O(N) total over all r.
        
        # Let's build the subsequence values
        sub = []
        idx = r
        while idx < n:
            sub.append(a[idx])
            idx += p
        
        k = len(sub)
        if k < m:
            continue
            
        # Sliding window on sub
        # Initial window: sub[0...m-1]
        window_counts = Counter()
        balance = 0
        
        # Helper to update balance
        # We need a function to update when count changes for a key
        
        # Initialize first window
        for i in range(m):
            val = sub[i]
            if val in b_keys:
                count_in_b = b_counter[val]
                current_count = window_counts[val]
                
                if current_count == count_in_b:
                    balance -= 1
                
                window_counts[val] += 1
                new_count = window_counts[val]
                
                if new_count == count_in_b:
                    balance += 1
                elif new_count > count_in_b:
                    # Now it exceeds, so it won't be equal. If it was equal before, balance decreased.
                    # If it wasn't equal before (either less or more), balance doesn't change due to equality check?
                    # Wait, the logic:
                    # balance counts how many keys have window_count == b_count.
                    # Before update: if current == b_count, balance includes this key.
                    # After update: if new == b_count, balance includes this key.
                    # So:
                    # if current == b_count: balance -= 1
                    # if new == b_count: balance += 1
                    pass
        
        # Check first window
        if balance == total_distinct_b:
            # Valid window starting at index 0 in sub
            # Original index = r + 0*p = r
            # q = r + 1
            valid_qs.append(r + 1)
        
        # Slide
        for i in range(k - m):
            # Remove sub[i]
            out_val = sub[i]
            if out_val in b_keys:
                count_in_b = b_counter[out_val]
                current_count = window_counts[out_val]
                
                if current_count == count_in_b:
                    balance -= 1
                
                window_counts[out_val] -= 1
                new_count = window_counts[out_val]
                
                if new_count == count_in_b:
                    balance += 1
            
            # Add sub[i+m]
            in_val = sub[i+m]
            if in_val in b_keys:
                count_in_b = b_counter[in_val]
                current_count = window_counts[in_val]
                
                if current_count == count_in_b:
                    balance -= 1
                
                window_counts[in_val] += 1
                new_count = window_counts[in_val]
                
                if new_count == count_in_b:
                    balance += 1
            
            # Check
            if balance == total_distinct_b:
                # Start index in sub is i + 1
                # Original index = r + (i + 1) * p
                # q = original_index + 1
                q_val = r + (i + 1) * p + 1
                valid_qs.append(q_val)

    valid_qs.sort()
    print(len(valid_qs))
    print(*(valid_qs))

if __name__ == '__main__':
    solve()