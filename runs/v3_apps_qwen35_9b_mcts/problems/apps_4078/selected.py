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

    # We need to maximize max(b) - min(b).
    # Since we can only decrease values, the maximum element in b will be one of the original a[i]
    # (possibly decreased if covered by chosen segments, but we can choose not to cover it).
    # Actually, the strategy is:
    # Fix the index `idx_max` which will become the maximum in the final array b.
    # Fix the index `idx_min` which will become the minimum in the final array b.
    # To ensure a[idx_max] is the maximum, we must NOT apply any segment that covers idx_max.
    # To ensure a[idx_min] is the minimum, we MUST apply ALL segments that cover idx_min.
    # Then we check if this configuration is valid (i.e., for all other i, b[i] is between min and max).
    # Actually, the condition is simpler:
    # We choose a set of segments S.
    # Let b[i] = a[i] - count of segments in S covering i.
    # We want to maximize max(b) - min(b).
    #
    # Observation: The optimal solution will have some index i being the unique maximum (or tied) and some j being the unique minimum (or tied).
    # If we fix i as the index of the maximum and j as the index of the minimum:
    # 1. We cannot apply any segment that covers i, otherwise b[i] decreases and might no longer be the max (or we reduce the gap).
    #    Wait, if we don't apply segments covering i, b[i] = a[i]. If we do apply, b[i] < a[i].
    #    To maximize the difference, we want b[i] as large as possible and b[j] as small as possible.
    #    So for the chosen max index i, we should NOT apply any segment covering it.
    #    For the chosen min index j, we SHOULD apply ALL segments covering it to make b[j] as small as possible.
    #
    # However, there is a catch: applying a segment covering j might also cover some other index k, reducing b[k].
    # If b[k] becomes smaller than b[j], then j is no longer the minimum.
    # So the condition is:
    # Let S be the set of ALL segments covering j.
    # We must NOT include any segment in S that covers i (because that would reduce b[i]).
    # So S = { all segments covering j } \ { segments covering both j and i }.
    # Then we calculate b for this S and check if max(b) - min(b) is indeed determined by i and j.
    # Specifically, we need:
    # b[i] >= b[k] for all k.
    # b[j] <= b[k] for all k.
    #
    # Algorithm:
    # Iterate over all pairs (i, j) with 0 <= i, j < n.
    #   Candidate set S = { s | s covers j }
    #   Remove from S any segment that covers i.
    #   Construct array b where b[k] = a[k] - (number of segments in S covering k).
    #   Check if b[i] >= max(b) and b[j] <= min(b).
    #   If valid, calculate diff = b[i] - b[j].
    #   Track the maximum diff and the corresponding set S.
    #
    # Complexity: O(N^2 * (M + N)). With N=300, M=300, this is roughly 300^2 * 600 = 5.4e7 operations, which might be tight for Python but acceptable for PyPy.
    # We can optimize the check using a difference array to compute b in O(N).
    
    # Precompute coverage counts for each segment to quickly check if a segment covers an index.
    # segments_covering[i] = list of segment indices that cover index i.
    segments_covering = [[] for _ in range(n)]
    for idx, (l, r, seg_id) in enumerate(segments):
        # 1-based l, r to 0-based
        l0, r0 = l - 1, r - 1
        for k in range(l0, r0 + 1):
            segments_covering[k].append(idx)

    max_diff = -1
    best_set = []
    best_i = -1
    best_j = -1

    # Optimization: Precompute which segments cover which indices is already done.
    # We can also precompute the "mask" of segments covering each index if M was small, but M=300 is too big for bitmask.
    # Just use lists.

    for i in range(n):
        for j in range(n):
            # We assume i is the max index and j is the min index.
            # Strategy:
            # 1. Take all segments covering j.
            # 2. Remove any segment that also covers i.
            # 3. Apply these segments.
            
            # Get candidate segments
            cand_indices = segments_covering[j]
            
            # Filter out segments that cover i
            # A segment covers i if i is in segments_covering[i]... wait, segments_covering[i] is the list of segments covering i.
            # So we need to check if a segment index is in segments_covering[i].
            # To make this O(1) or O(log M), we can convert segments_covering[i] to a set.
            # But doing this inside the loop is expensive.
            # Let's precompute sets for each index.
            pass

    # Precompute sets for fast lookup
    segments_covering_set = [set(lst) for lst in segments_covering]

    for i in range(n):
        for j in range(n):
            # Candidate segments: those covering j but NOT covering i
            # We can iterate over segments_covering[j] and check membership in segments_covering_set[i]
            
            # Build the set of active segment indices
            active_segments = []
            for seg_idx in segments_covering[j]:
                if seg_idx not in segments_covering_set[i]:
                    active_segments.append(seg_idx)
            
            if not active_segments:
                # If no segments are applied, diff is 0.
                # But we might find a better diff later.
                # However, if active_segments is empty, b = a, diff = max(a) - min(a).
                # We can handle this case generally.
                pass
            
            # Calculate b using difference array for O(N)
            diff_arr = [0] * (n + 2)
            for seg_idx in active_segments:
                l, r, _ = segments[seg_idx]
                l0, r0 = l - 1, r - 1
                diff_arr[l0] += 1
                diff_arr[r0 + 1] -= 1
            
            current_b = [0] * n
            curr = 0
            for k in range(n):
                curr += diff_arr[k]
                current_b[k] = a[k] - curr
            
            # Check conditions
            # b[i] must be >= all elements
            # b[j] must be <= all elements
            
            # Check max
            is_max = True
            for k in range(n):
                if current_b[k] > current_b[i]:
                    is_max = False
                    break
            
            if not is_max:
                continue
            
            # Check min
            is_min = True
            for k in range(n):
                if current_b[k] < current_b[j]:
                    is_min = False
                    break
            
            if not is_min:
                continue
            
            # Valid configuration
            d = current_b[i] - current_b[j]
            if d > max_diff:
                max_diff = d
                best_set = active_segments
                best_i = i
                best_j = j
            elif d == max_diff and max_diff != -1:
                # We can keep the first one or update, doesn't matter.
                pass

    # Output results
    print(max_diff)
    print(len(best_set))
    # Convert segment indices (0-based) to 1-based and print
    print(*(x + 1 for x in best_set))

if __name__ == '__main__':
    solve()