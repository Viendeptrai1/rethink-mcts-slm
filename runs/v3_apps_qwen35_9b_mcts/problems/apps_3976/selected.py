import sys
from collections import Counter

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        p = int(next(iterator))
        
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
            
        b = []
        for _ in range(m):
            b.append(int(next(iterator)))
    except StopIteration:
        return

    if m > n:
        print(0)
        print()
        return

    b_counter = Counter(b)
    
    # We need to check for each residue class r in [0, p-1]
    # The indices in 'a' that belong to residue class r are those where (i+1) % p == r+1 (1-based)
    # Or simply: index i (0-based) belongs to residue class (i+1) % p.
    # Let's group indices by (i+1) % p.
    
    # We will store lists of indices for each residue class
    # residues[r] will contain a sorted list of 0-based indices i such that (i+1) % p == r
    residues = [[] for _ in range(p)]
    
    for idx, val in enumerate(a):
        r = (idx + 1) % p
        residues[r].append(idx)
    
    valid_qs = []
    
    for r in range(p):
        indices = residues[r]
        if not indices:
            continue
            
        # We need to check starting positions q such that q % p == r (if r != 0) or q % p == 0 (if r == 0)
        # Actually, the condition is: the sequence starts at a[q-1] (0-based index q-1).
        # The indices accessed are: q-1, q-1+p, q-1+2p, ..., q-1+(m-1)p.
        # All these indices must have the same residue modulo p.
        # Specifically, (q-1) % p must be equal to r.
        # So q-1 = k*p + r => q = k*p + r + 1.
        # Since q >= 1, and indices are 0-based, let's map carefully.
        # If we use 0-based index 'start' for the first element:
        # start, start+p, start+2p, ... start+(m-1)p
        # All these must be in the 'indices' list for residue class (start+1)%p.
        # Note: (start + k*p + 1) % p = (start+1)%p. So yes, they all share the same residue class.
        
        # We need to find 'start' in 'indices' such that the subsequence starting at 'start' with step p
        # contains exactly the multiset of values in 'b'.
        
        # Optimization: Instead of checking every start, we can use a sliding window approach on the 'indices' list.
        # However, the values are not contiguous in the original array, but they are contiguous in the 'indices' list.
        # Let's extract the values corresponding to 'indices'.
        vals = [a[i] for i in indices]
        
        # Now the problem reduces to: in array 'vals', find starting positions 'k' (0-based in 'vals')
        # such that the subarray vals[k : k+m] is a permutation of 'b'.
        # But wait, the step in 'a' is p, which corresponds to step 1 in 'indices' because 'indices' is sorted.
        # indices[j] = indices[j-1] + p. Yes, because we collected all indices with the same residue in increasing order.
        # So checking vals[k : k+m] is exactly checking a[start], a[start+p], ..., a[start+(m-1)p].
        
        if len(vals) < m:
            continue
            
        # We need to count matches efficiently.
        # Since values can be large, we use a Counter.
        # We can use a sliding window with a "balance" counter.
        
        target = b_counter
        current = Counter()
        
        # Initialize window [0, m-1]
        for i in range(m):
            current[vals[i]] += 1
            
        # Check first window
        if current == target:
            # The starting index in 'a' is indices[0]
            # q = indices[0] + 1
            valid_qs.append(indices[0] + 1)
            
        # Slide window
        for i in range(m, len(vals)):
            # Remove element leaving the window: vals[i-m]
            out_val = vals[i-m]
            current[out_val] -= 1
            if current[out_val] == 0:
                del current[out_val]
                
            # Add element entering the window: vals[i]
            in_val = vals[i]
            current[in_val] += 1
            
            if current == target:
                # The starting index in 'a' is indices[i-m+1]
                valid_qs.append(indices[i-m+1] + 1)
                
    valid_qs.sort()
    print(len(valid_qs))
    print(*(valid_qs))

if __name__ == '__main__':
    solve()