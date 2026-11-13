import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    m = int(next(iterator))
    
    queries = []
    for _ in range(m):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r))
    
    # Calculate the maximum possible minimum mex
    # The key insight is that for any subarray of length L, the mex is at most L.
    # To maximize the minimum mex over all queries, we want to find the smallest length among all queries.
    # Let min_len be the minimum length of any query subarray.
    # We can construct an array such that every subarray of length >= min_len has a mex of at least min_len.
    # Actually, if we have a subarray of length L, the mex cannot exceed L.
    # So the answer is bounded by min_len.
    # Can we always achieve min_len?
    # Yes. If we assign values 0, 1, 2, ... cyclically or in a way that covers [0, min_len-1] in every window of size min_len.
    # A simple pattern that works for any window of size >= K is to repeat 0, 1, ..., K-1.
    # If a window has length L >= K, and we have a repeating pattern of 0..K-1, does it guarantee mex >= K?
    # Not necessarily with just 0..K-1 repeating if the window doesn't align.
    # However, consider the constraint: we need mex >= K for ALL queried subarrays.
    # The most restrictive subarray is the one with the smallest length, say L_min.
    # Its mex is at most L_min. So the answer is at most L_min.
    # Can we achieve L_min?
    # Yes. We can set a[i] = i % (L_min).
    # Then any subarray of length L >= L_min will contain all numbers from 0 to L_min-1?
    # Let's check: Pattern 0, 1, 2, ..., L_min-1, 0, 1, ...
    # Any contiguous subarray of length L_min contains exactly one of each 0, 1, ..., L_min-1.
    # Thus mex is L_min.
    # Any subarray of length > L_min also contains all numbers 0..L_min-1 (since it contains a full cycle), so mex >= L_min.
    # Therefore, the optimal answer is exactly the minimum length of the given subarrays.
    
    min_len = float('inf')
    for l, r in queries:
        length = r - l + 1
        if length < min_len:
            min_len = length
    
    # If there are no queries, technically the problem says m >= 1, so min_len will be set.
    # But just in case:
    if min_len == float('inf'):
        print(0)
        print(*(0 for _ in range(n)))
        return

    ans_mex = min_len
    # Construct the array
    # Pattern: 0, 1, 2, ..., ans_mex-1, 0, 1, ...
    arr = [i % ans_mex for i in range(n)]
    
    print(ans_mex)
    print(*(arr))

if __name__ == '__main__':
    solve()