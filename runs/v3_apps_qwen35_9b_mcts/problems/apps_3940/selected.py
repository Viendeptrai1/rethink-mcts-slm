import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    queries = []
    for _ in range(m):
        l = int(next(iterator))
        r = int(next(iterator))
        queries.append((l, r))
    
    # We need to find the maximum k such that for every query (l, r),
    # the subarray a[l..r] contains all integers from 0 to k-1.
    # This is equivalent to saying that for every query, the length (r - l + 1) must be >= k.
    # Why? Because if a subarray has length L, the maximum possible mex it can have is L+1 (if it contains 0..L-1).
    # However, we are constructing the array. We want to assign values such that the minimum mex over all queries is maximized.
    # 
    # Key Insight:
    # If we have a query of length L, the best we can do for that specific query is to have mex = L+1 (by filling 0, 1, ..., L-1).
    # But we have multiple overlapping queries.
    # Consider the shortest query length among all given queries. Let min_len = min(r_i - l_i + 1).
    # Can we achieve a minimum mex of min_len?
    # Yes. If we construct the array such that every contiguous subsegment of length min_len contains 0, 1, ..., min_len-1,
    # then any query of length >= min_len will definitely contain 0, 1, ..., min_len-1 (since it contains a subsegment of length min_len).
    # Thus, the mex of any query will be at least min_len + 1? Wait.
    # Definition: mex is the smallest non-negative integer NOT in the set.
    # If a set contains {0, 1, ..., k-1}, the mex is k.
    # If a subarray has length L, and we fill it with 0, 1, ..., L-1, the mex is L.
    # So if the shortest query has length L_min, we can ensure its mex is L_min.
    # Any other query has length L >= L_min. If we construct the array carefully, can we ensure its mex is also >= L_min?
    # Actually, the constraint is simpler:
    # The answer is simply the length of the shortest query.
    # Let's verify with Example 1:
    # Queries: [1,3] (len 3), [2,5] (len 4), [4,5] (len 2).
    # Shortest length is 2. Output says 2. Correct.
    # Example 2:
    # Queries: [1,4] (len 4), [2,4] (len 3).
    # Shortest length is 3. Output says 3. Correct.
    #
    # Construction Strategy:
    # We need to fill the array such that every window of size K (where K = min_len) contains 0, 1, ..., K-1.
    # A simple periodic pattern works: a[i] = i % K.
    # Let's check if a[i] = i % K satisfies the condition.
    # Consider any subarray of length K starting at index s: a[s], a[s+1], ..., a[s+K-1].
    # The values are s%K, (s+1)%K, ..., (s+K-1)%K.
    # This is a permutation of 0, 1, ..., K-1.
    # So the mex is K.
    # Now consider a query of length L > K. It contains multiple windows of size K.
    # Does it contain 0, 1, ..., K-1? Yes, because it contains at least one full window of size K which has all these values.
    # Therefore, the mex of any query of length >= K will be at least K.
    # The minimum mex will be exactly K (achieved by the shortest query).
    #
    # So the algorithm is:
    # 1. Find the minimum length among all queries. Let this be K.
    # 2. The answer is K.
    # 3. Construct the array a where a[i] = i % K (using 0-based indexing for calculation, but input is 1-based).
    #    Specifically, for the i-th element (1-based index i), value is (i-1) % K.
    
    min_len = float('inf')
    for l, r in queries:
        length = r - l + 1
        if length < min_len:
            min_len = length
            
    k = min_len
    print(k)
    
    # Construct array
    # a[i] for i from 1 to n
    # value = (i-1) % k
    res = []
    for i in range(1, n + 1):
        res.append((i - 1) % k)
        
    print(*(res))

if __name__ == '__main__':
    solve()