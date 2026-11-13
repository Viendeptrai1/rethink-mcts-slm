import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    queries = []
    for _ in range(m):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r))

    # We need to find the maximum possible minimum mex.
    # The mex of a subarray of length L is at most L.
    # If we can fill the array such that every query subarray of length L contains
    # all numbers from 0 to L-1, then the mex will be L.
    # However, we have multiple overlapping constraints.
    #
    # Key Insight:
    # Consider the length of each query subarray: len = r - l + 1.
    # The mex of this subarray cannot exceed its length.
    # Therefore, the minimum mex over all queries cannot exceed the minimum length among all queries.
    # Let min_len = min(r_i - l_i + 1) for all i.
    # The answer is at most min_len.
    #
    # Can we always achieve min_len?
    # Yes. We can construct the array by filling it with a repeating pattern 0, 1, 2, ..., k-1, 0, 1, ...
    # where k = min_len.
    # Specifically, a[i] = i % k (using 0-based indexing for the array, but queries are 1-based).
    #
    # Let's verify:
    # Take any query [l, r] with length L = r - l + 1.
    # The subarray elements will be (l-1)%k, l%k, ..., (r-1)%k.
    # Since the pattern repeats every k numbers, any contiguous segment of length L >= k will contain
    # a full cycle of 0, 1, ..., k-1.
    # Thus, the set of values in the subarray will include {0, 1, ..., k-1}.
    # The mex will be at least k.
    # Since the length is L, the mex is at most L.
    # So the mex is exactly k if L >= k.
    #
    # What if L < k?
    # This is impossible because k is defined as the minimum length among all queries.
    # So for all queries, L >= k.
    # Therefore, the mex for every query will be at least k.
    # And since there exists at least one query with length k, its mex will be exactly k (because it has k elements, so it can't have mex > k, and it contains 0..k-1 so mex >= k).
    #
    # Conclusion: The maximum possible minimum mex is exactly min_len.
    # The construction is a[i] = (i) % min_len for i from 0 to n-1.

    min_len = float('inf')
    for l, r in queries:
        length = r - l + 1
        if length < min_len:
            min_len = length

    # Construct the array
    result = []
    k = min_len
    for i in range(n):
        result.append(i % k)

    # Output
    print(k)
    print(*(result))

if __name__ == '__main__':
    solve()