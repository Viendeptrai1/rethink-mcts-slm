import sys
from collections import Counter

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    m = int(next(iterator))
    p = int(next(iterator))

    a = []
    for _ in range(n):
        a.append(int(next(iterator)))

    b = []
    for _ in range(m):
        b.append(int(next(iterator)))

    if m == 0:
        # If b is empty, technically any q satisfying the condition works?
        # But constraints say m >= 1, so this case won't happen per problem statement.
        print(0)
        print()
        return

    # Count frequencies in b
    b_count = Counter(b)
    total_b = len(b_count)

    # We need to check positions q such that the subsequence a[q-1], a[q-1+p], ... matches b as a multiset.
    # The indices in a involved are: q-1, q-1+p, q-1+2p, ..., q-1+(m-1)p
    # These indices all have the same value modulo p.
    # So we can process each remainder r in [0, p-1] independently.

    valid_qs = []

    # Precompute counts for b
    # We will use a sliding window approach on each remainder chain.
    # For a fixed remainder r, the chain is: r, r+p, r+2p, ... (0-indexed)
    # Let this chain be c_0, c_1, c_2, ...
    # We need a window of length m starting at index k in this chain.
    # The window corresponds to original indices: k, k+p, k+2p, ...
    # The starting position q (1-based) would be k + 1.
    # Condition: q + (m-1)*p <= n  =>  k + 1 + (m-1)*p <= n  =>  k <= n - 1 - (m-1)*p
    # Also k >= 0.

    # To efficiently check if the current window matches b_count:
    # We maintain a counter of the current window.
    # We also maintain a variable `matches` which counts how many distinct elements
    # have the correct frequency in the current window compared to b_count.
    # Or simpler: maintain a count of "satisfied" elements.
    # An element x is satisfied if window_count[x] == b_count[x].
    # We also need to know if all elements in b_count are satisfied AND no extra elements exist.
    # Since the window size is fixed at m, if the sum of frequencies of satisfied elements equals m,
    # and we have satisfied all keys in b_count, then it's a match.
    # Actually, simpler logic:
    # Let's track `diff_count`: number of elements where window_count != b_count.
    # Initially 0.
    # When adding an element x:
    #   old_diff = (window_count[x] != b_count[x])
    #   window_count[x] += 1
    #   new_diff = (window_count[x] != b_count[x])
    #   if old_diff and not new_diff: diff_count -= 1
    #   elif not old_diff and new_diff: diff_count += 1
    # When removing an element x:
    #   old_diff = (window_count[x] != b_count[x])
    #   window_count[x] -= 1
    #   new_diff = (window_count[x] != b_count[x])
    #   if old_diff and not new_diff: diff_count -= 1
    #   elif not old_diff and new_diff: diff_count += 1
    # Match if diff_count == 0.

    # However, we must also ensure that we don't have extra elements not in b?
    # If diff_count == 0, it means for every x, window_count[x] == b_count[x].
    # This implies the window has exactly the same multiset as b.
    # So diff_count == 0 is sufficient.

    # Optimization: Instead of full Counter for every step, we can just track the diff_count.
    # But we need to know b_count[x] quickly. A dict is fine.

    b_counts = dict(b_count)
    # Pre-calculate the max index for each remainder
    # Max valid start index k (0-based) for a chain is: n - 1 - (m-1)*p
    max_k = n - 1 - (m - 1) * p
    if max_k < 0:
        print(0)
        print()
        return

    # We will iterate r from 0 to p-1
    # For each r, build the chain of indices: r, r+p, r+2p, ...
    # Then slide a window of size m.

    # To avoid creating many lists, we can iterate directly.
    
    # We need a way to quickly access a[i].
    # a is already a list.

    # Let's implement the sliding window for each remainder.
    
    # We can reuse the window_count dict and diff_count variable to save allocation time?
    # But creating a new dict for each remainder might be slow if p is large.
    # However, the total number of elements across all chains is n.
    # So O(n) operations total is fine.
    
    # Let's use a single dictionary for window counts and reset it for each remainder.
    # Actually, creating a new dict for each remainder is O(number of unique elements in that chain).
    # Sum of unique elements over all chains <= n. So it's fine.

    for r in range(p):
        # Build the chain indices
        # We only care about indices <= max_k + (m-1)*p? 
        # Actually, the chain goes up to n-1.
        # The valid windows start at k where k + (m-1)*p <= n-1.
        # So the last element of the window is at index k + (m-1)*p.
        # The maximum index we ever access is n-1.
        
        # Collect elements in the chain
        chain = []
        idx = r
        while idx < n:
            chain.append(a[idx])
            idx += p
        
        # If chain length is less than m, no window possible
        if len(chain) < m:
            continue
        
        # Sliding window on chain
        # Window size is m
        # Initial window: chain[0...m-1]
        
        window_counts = {}
        diff_count = 0
        
        # Initialize first window
        for i in range(m):
            val = chain[i]
            target = b_counts.get(val, 0)
            current = window_counts.get(val, 0)
            
            # Before increment
            if current == target:
                diff_count += 1
            # Increment
            window_counts[val] = current + 1
            # After increment
            new_current = window_counts[val]
            if new_current == target:
                diff_count -= 1
            elif new_current != target:
                # It was not equal before (since we incremented from current which was not target)
                # Wait, logic check:
                # If current != target, then it contributed to diff_count.
                # After increment, if new_current == target, it stops contributing -> diff_count decreases.
                # If new_current != target, it still contributes -> diff_count unchanged.
                pass
        
        # Re-evaluate diff_count logic more carefully
        # Let's restart the initialization logic to be robust.
        
        # Reset
        window_counts = {}
        diff_count = 0
        
        # Helper to update diff_count
        def update_add(val):
            nonlocal diff_count
            target = b_counts.get(val, 0)
            current = window_counts.get(val, 0)
            
            # Before
            if current == target:
                diff_count += 1 # It was matching, now it won't (unless target increases, but target is fixed)
                # Wait, if current == target, then it was NOT contributing to diff_count.
                # So if we change it, it WILL contribute.
                # So diff_count increases by 1.
            
            window_counts[val] = current + 1
            new_current = window_counts[val]
            
            # After
            if new_current == target:
                diff_count -= 1 # It was not matching (or was matching? no, if it was matching, current==target, then new_current != target)
                # If current == target, then new_current = target+1 != target. So it stops matching.
                # If current != target, and new_current == target, it starts matching.
            
            # Let's simplify:
            # Contribution to diff_count is 1 if current != target, else 0.
            # Old contribution: (current != target)
            # New contribution: (new_current != target)
            # diff_count = diff_count - old_contrib + new_contrib
            
            old_contrib = 1 if current != target else 0
            new_contrib = 1 if new_current != target else 0
            diff_count = diff_count - old_contrib + new_contrib

        def update_remove(val):
            nonlocal diff_count
            target = b_counts.get(val, 0)
            current = window_counts.get(val, 0)
            
            old_contrib = 1 if current != target else 0
            current -= 1
            new_current = current
            new_contrib = 1 if new_current != target else 0
            
            window_counts[val] = new_current
            if new_current == 0:
                del window_counts[val]
            
            diff_count = diff_count - old_contrib + new_contrib

        # Initialize first window
        for i in range(m):
            update_add(chain[i])
        
        if diff_count == 0:
            valid_qs.append(r + 1) # q = r + 1 (since r is 0-based index in chain, which corresponds to 0-based index in a)
            # Wait, q is 1-based index in a.
            # Chain index 0 corresponds to a[r].
            # If window starts at chain index k, it corresponds to a[r + k*p].
            # The problem asks for q such that the sequence starts at a[q-1].
            # So if the window starts at chain index k, then a[q-1] = a[r + k*p] => q-1 = r + k*p => q = r + k*p + 1.
            # Here k=0, so q = r + 1. Correct.

        # Slide window
        # We have a window from k=0 to k=m-1.
        # Next window starts at k=1, ends at k=m.
        # Remove chain[0], add chain[m]
        
        # The valid start indices k in the chain are from 0 to len(chain) - m.
        # We already checked k=0.
        # Loop k from 1 to len(chain) - m
        
        limit = len(chain) - m
        for k in range(1, limit + 1):
            remove_val = chain[k - 1]
            add_val = chain[k + m - 1]
            
            update_remove(remove_val)
            update_add(add_val)
            
            if diff_count == 0:
                # Start index in chain is k
                # q = r + k*p + 1
                q = r + k * p + 1
                valid_qs.append(q)

    valid_qs.sort()
    print(len(valid_qs))
    print(*(valid_qs))

if __name__ == '__main__':
    solve()