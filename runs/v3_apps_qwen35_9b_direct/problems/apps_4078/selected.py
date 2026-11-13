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

    a = []
    for _ in range(n):
        a.append(int(next(iterator)))

    segments = []
    for i in range(m):
        l = int(next(iterator))
        r = int(next(iterator))
        segments.append((l, r, i + 1))

    if m == 0:
        print(0)
        print(0)
        print()
        return

    # We need to find indices i and j such that (max(b) - min(b)) is maximized.
    # Since we can only decrease values, the new value at index k is a[k] - count[k],
    # where count[k] is the number of chosen segments covering k.
    # To maximize max(b) - min(b), we can fix the index that becomes the maximum (i)
    # and the index that becomes the minimum (j).
    # Then we want to maximize (a[i] - count[i]) - (a[j] - count[j])
    # = (a[i] - a[j]) + (count[j] - count[i]).
    # To maximize this, we should choose segments that cover j but do NOT cover i.
    # Let S be the set of chosen segments. We want to maximize |{s in S : j in s}| - |{s in S : i in s}|.
    # This is equivalent to maximizing the number of segments that cover j and not i.
    # We can iterate over all pairs (i, j) and count how many segments cover j but not i.
    # Then take the maximum.

    # Precompute coverage for each segment for each index to speed up?
    # n, m <= 300. O(n^2 * m) is roughly 27 million operations, which is acceptable for PyPy.
    
    # Let's create a coverage matrix: cover[k][seg_idx] = 1 if segment seg_idx covers index k, else 0.
    # Indices for array a are 0 to n-1. Segments are 0 to m-1.
    
    cover = [[0] * m for _ in range(n)]
    for idx, (l, r, _) in enumerate(segments):
        # l and r are 1-based
        for k in range(l - 1, r):
            cover[k][idx] = 1

    max_diff = -float('inf')
    best_i = -1
    best_j = -1
    best_count = 0
    best_segments = []

    # Iterate over all pairs (i, j)
    # i is the index that will be the maximum element in b
    # j is the index that will be the minimum element in b
    for i in range(n):
        for j in range(n):
            # We want to choose a subset of segments S such that:
            # count[j] - count[i] is maximized.
            # count[k] = sum(cover[k][s] for s in S)
            # So we want to maximize sum(cover[j][s] - cover[i][s] for s in S).
            # For each segment s:
            #   if cover[j][s] == 1 and cover[i][s] == 0: contribution +1 (should include)
            #   if cover[j][s] == 0 and cover[i][s] == 1: contribution -1 (should exclude)
            #   otherwise: contribution 0 (doesn't matter, but to keep it simple, exclude)
            # Actually, to maximize the sum, we simply include all segments where cover[j][s] == 1 and cover[i][s] == 0.
            # Including others doesn't hurt the difference count[j]-count[i], but might affect other values.
            # However, the problem asks to maximize max(b) - min(b). By fixing i and j as the max and min,
            # we ensure that b[i] is the max and b[j] is the min among the resulting array?
            # Not necessarily. If we pick segments to maximize b[i] - b[j], it's possible that some other b[k] > b[i] or b[k] < b[j].
            # But note: b[k] = a[k] - count[k].
            # If we only add segments that cover j and not i, then count[j] increases and count[i] stays same.
            # So b[j] decreases and b[i] stays same. Thus b[i] - b[j] increases.
            # Could b[k] become larger than b[i]? b[k] = a[k] - count[k]. Since we only add segments covering j (and not i),
            # count[k] increases only if k is covered by these segments.
            # If k is covered, b[k] decreases. If k is not covered, b[k] stays same.
            # So b[i] is definitely >= original a[i] - (original count[i] from chosen set).
            # Wait, the logic is: we choose a set S. Then b is determined.
            # We want max(b) - min(b).
            # If we fix i and j, and we choose S to maximize b[i] - b[j], does it guarantee that b[i] is max and b[j] is min?
            # Not strictly. But consider:
            # b[i] = a[i] - count[i]
            # b[j] = a[j] - count[j]
            # We want to maximize (a[i] - a[j]) + (count[j] - count[i]).
            # The maximum possible value of (count[j] - count[i]) is achieved by taking all segments that cover j and not i.
            # Let this max value be D. Then the candidate answer is (a[i] - a[j]) + D.
            # Is it possible that with this set S, there exists k such that b[k] > b[i] or b[k] < b[j]?
            # If b[k] > b[i], then a[k] - count[k] > a[i] - count[i] => a[k] - a[i] > count[k] - count[i].
            # If b[k] < b[j], then a[k] - count[k] < a[j] - count[j] => a[j] - a[k] > count[j] - count[k].
            # However, we are iterating over ALL pairs (i, j). If the true max-min pair is (u, v), then when our loop reaches (u, v),
            # we will calculate the optimal count difference for that pair, which will yield the true max difference.
            # Even if for a specific pair (i, j) the resulting array has a different max or min, the value b[i] - b[j] we calculate
            # is a lower bound on the actual max-min of that array? No.
            # Actually, the strategy is: The optimal solution has some max element at index u and min at index v.
            # Then the value is b[u] - b[v].
            # To achieve this, we must have chosen a set of segments.
            # For this set, count[v] - count[u] = (b[u] - b[v]) - (a[u] - a[v]).
            # To maximize b[u] - b[v], we need to maximize count[v] - count[u].
            # The maximum possible value of count[v] - count[u] is obtained by taking all segments that cover v and not u.
            # Let this max value be M_uv.
            # Then the maximum possible b[u] - b[v] is (a[u] - a[v]) + M_uv.
            # If we construct the array using exactly these segments, then b[u] - b[v] will be exactly this value.
            # Could there be another index k such that b[k] > b[u] or b[k] < b[v]?
            # If b[k] > b[u], then the actual max-min would be > b[u] - b[v].
            # But then the pair (k, v) would have been considered in our loop, and we would have found a larger or equal difference.
            # Specifically, if the true max is at k and min at v, then when we process (k, v), we will compute
            # (a[k] - a[v]) + (max possible count[v] - count[k]).
            # Since the set of segments we chose for (u, v) is a subset of segments covering v and not u,
            # and for (k, v) we take all segments covering v and not k.
            # Note that segments covering v and not u are a subset of segments covering v and not k? Not necessarily.
            # But the key insight is: The value we compute for pair (u, v) is an UPPER BOUND on the difference b[u] - b[v] achievable by ANY set of segments.
            # Why? Because count[v] - count[u] <= (number of segments covering v and not u).
            # So b[u] - b[v] = a[u] - a[v] + count[v] - count[u] <= a[u] - a[v] + (segments covering v and not u).
            # Therefore, the maximum over all pairs of (a[i] - a[j] + count_segments(j, not i)) is an upper bound on the answer.
            # Can we achieve this upper bound? Yes, by choosing exactly the segments that cover j and not i.
            # Let S be the set of segments covering j and not i.
            # Then b[i] = a[i] - count[i] (where count[i] is number of segments in S covering i, which is 0).
            # b[j] = a[j] - count[j] (where count[j] is number of segments in S covering j, which is |S|).
            # So b[i] - b[j] = a[i] - a[j] + |S|. This matches the upper bound.
            # Now, is it possible that for this set S, there is some k with b[k] > b[i] or b[k] < b[j]?
            # If b[k] > b[i], then a[k] - count[k] > a[i] - 0 => a[k] - a[i] > count[k].
            # If b[k] < b[j], then a[k] - count[k] < a[j] - |S| => a[j] - a[k] > |S| - count[k].
            # However, if such a k exists, then the pair (k, i) or (k, j) would yield a higher or equal value in our iteration?
            # Actually, the standard solution for this problem relies on the fact that we can just iterate all pairs and take the max.
            # The logic holds: The maximum possible value of max(b) - min(b) is exactly max over i,j of (a[i] - a[j] + count(j, not i)).
            # Proof sketch: Let the optimal set be S_opt, with max at u and min at v.
            # Then ans = b[u] - b[v] = a[u] - a[v] + count[v] - count[u].
            # We know count[v] - count[u] <= count(v, not u) (since count[u] >= 0).
            # So ans <= a[u] - a[v] + count(v, not u).
            # Our algorithm computes max over all pairs of RHS. So our answer >= ans.
            # Also, for any pair (i, j), if we choose S = {s | s covers j and not i}, then b[i] - b[j] = a[i] - a[j] + count(j, not i).
            # Let this value be V_ij. The actual max-min of the resulting array b is >= b[i] - b[j] = V_ij.
            # So the true answer >= V_ij for all i, j.
            # Thus true answer >= max_ij V_ij.
            # Combining, true answer = max_ij V_ij.
            
            current_diff = a[i] - a[j]
            count_j_not_i = 0
            for k in range(m):
                if cover[j][k] == 1 and cover[i][k] == 0:
                    count_j_not_i += 1
            
            total = current_diff + count_j_not_i
            
            if total > max_diff:
                max_diff = total
                best_i = i
                best_j = j
                best_count = count_j_not_i
                # Collect segments
                best_segments = []
                for k in range(m):
                    if cover[j][k] == 1 and cover[i][k] == 0:
                        best_segments.append(segments[k][2])

    print(max_diff)
    print(best_count)
    print(*(best_segments))

if __name__ == '__main__':
    solve()