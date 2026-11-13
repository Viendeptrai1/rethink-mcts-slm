import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[1 + i]))
    
    # Count frequency of each height
    from collections import Counter
    counts = Counter(a)
    
    # Find the maximum possible range [h, h+1]
    # The maximum number of people we can pick is counts[h] + counts[h+1]
    # We iterate over all unique heights present and find the max sum for consecutive pairs.
    
    if n == 1:
        print(1)
        print(a[0])
        return

    # Get sorted unique heights
    unique_heights = sorted(counts.keys())
    
    max_k = 0
    best_start = -1
    
    # Check pairs (h, h+1)
    for i in range(len(unique_heights) - 1):
        h1 = unique_heights[i]
        h2 = unique_heights[i+1]
        if h2 == h1 + 1:
            k = counts[h1] + counts[h2]
            if k > max_k:
                max_k = k
                best_start = h1
    
    # Check single heights (if no pair exists or single is better, though single is always <= pair if pair exists)
    # Actually, if only one unique height exists, the loop above won't run, so we handle it.
    if max_k == 0:
        # Only one unique height or no consecutive pairs
        # In this case, we can just take all people of that height
        # The best single height is the one with max count
        for h in unique_heights:
            if counts[h] > max_k:
                max_k = counts[h]
                best_start = h
    
    # Construct the result
    # Order: h, h+1, h, h+1, ... then close the loop properly.
    # Actually, the sequence should be: h, h+1, h, h+1, ... until we use all.
    # To satisfy circular condition: last element must be within 1 of first.
    # If we have only h's: h, h, h -> |h-h|<=1 ok.
    # If we have h and h+1: 
    # Option 1: h, h+1, h, h+1... 
    # If count(h) == count(h+1): h, h+1, h, h+1 ... ends with h+1. |h+1 - h| = 1. OK.
    # If count(h) > count(h+1): h, h+1, h, h+1 ... h (ends with h). |h - h| = 0. OK.
    # If count(h+1) > count(h): h, h+1, h, h+1 ... h+1 (ends with h+1). |h+1 - h| = 1. OK.
    
    # Strategy:
    # Print all h, then all h+1? No, that would be h, h, h, h+1, h+1. 
    # |h - h+1| = 1 ok. |h+1 - h| = 1 ok.
    # But wait, the transition from last h+1 to first h is |h+1 - h| = 1. OK.
    # So simple concatenation: [all h] + [all h+1] works.
    # Let's verify:
    # Sequence: h, h, ..., h, h+1, h+1, ..., h+1
    # Adjacent diffs:
    # h to h: 0
    # h to h+1: 1
    # h+1 to h+1: 0
    # Last (h+1) to First (h): 1
    # This works perfectly.
    
    res = []
    h = best_start
    h_next = h + 1
    
    count_h = counts[h]
    count_h_next = counts[h_next] if h_next in counts else 0
    
    # If best_start was determined from a pair, both counts > 0.
    # If best_start was determined from a single, then count_h_next = 0.
    
    # Append all h
    for _ in range(count_h):
        res.append(h)
    
    # Append all h+1
    for _ in range(count_h_next):
        res.append(h_next)
        
    print(max_k)
    print(*(res))

if __name__ == '__main__':
    solve()