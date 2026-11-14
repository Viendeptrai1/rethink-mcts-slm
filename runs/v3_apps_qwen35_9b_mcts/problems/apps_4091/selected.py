import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = []
    for i in range(n):
        a.append(int(data[2 + i]))
    
    # The strategy is to find the k largest elements in the array.
    # These k elements will be the maximums of the k segments.
    # To maximize the sum, we simply take the k largest values.
    # Since we need to output the partition sizes, we can construct it greedily.
    # We sort the array to find the threshold for the k-th largest element.
    # However, we must preserve the original indices to form contiguous segments.
    
    # Create a list of (value, original_index)
    indexed_a = [(a[i], i) for i in range(n)]
    # Sort by value descending
    indexed_a.sort(key=lambda x: x[0], reverse=True)
    
    # Take the top k elements
    top_k = indexed_a[:k]
    
    # The total profit is the sum of these k values
    total_profit = sum(x[0] for x in top_k)
    
    # Now we need to construct the partition.
    # We have k segments. The maximum of each segment must be one of the top_k elements.
    # We can assign the first segment to end at the index of the first top_k element.
    # The second segment to end at the index of the second top_k element, and so on.
    # The last segment will go from the index after the (k-1)-th top_k element to the end of the array.
    # This ensures that each segment contains exactly one of the top_k elements as its maximum (or at least, the max is >= the required value, and since we picked the largest available, the sum is maximized).
    # Actually, the logic is simpler: 
    # We sort the top_k elements by their original index to determine the order of segments.
    # Let the sorted top_k indices be idx_0, idx_1, ..., idx_{k-1}.
    # Segment 1: from 0 to idx_0 (inclusive) -> max is a[idx_0] (which is in top_k)
    # Segment 2: from idx_0 + 1 to idx_1 (inclusive) -> max is a[idx_1]
    # ...
    # Segment k: from idx_{k-2} + 1 to n-1 (inclusive) -> max is a[idx_{k-1}]
    # Note: The segment from idx_{k-2}+1 to idx_{k-1} has max a[idx_{k-1}].
    # The last segment goes from idx_{k-2}+1 to n-1. Its max will be at least a[idx_{k-1}] because a[idx_{k-1}] is in it.
    # Wait, if there are other large values in the last segment that are NOT in top_k? 
    # No, because top_k contains the k largest values in the entire array. Any value not in top_k is <= the smallest value in top_k.
    # So the max of any segment formed this way will be exactly the value of the top_k element that defines its right boundary (except possibly the last segment if there's a larger value before the last top_k element? No, because we sorted top_k by index).
    # Let's re-verify:
    # We pick the k largest values. Let their indices be p_0 < p_1 < ... < p_{k-1}.
    # We form segments: [0, p_0], [p_0+1, p_1], ..., [p_{k-2}+1, p_{k-1}], [p_{k-1}+1, n-1].
    # Segment 1 max: max(a[0]...a[p_0]). Since a[p_0] is in top_k and is the largest in the whole array? Not necessarily the largest overall, but it is one of the k largest.
    # Is it possible that a[0]...a[p_0-1] contains a value larger than a[p_0]?
    # If there was a value larger than a[p_0] before p_0, then that value would be in top_k (since top_k has the k largest). But p_0 is the index of the first element in top_k. So no element before p_0 can be in top_k. Thus, all elements before p_0 are <= the k-th largest value.
    # Actually, a[p_0] is the largest among {a[p_0]} U {elements before p_0 that are NOT in top_k}.
    # Since all elements in top_k are >= any element not in top_k, and a[p_0] is in top_k, then a[p_0] >= any element before p_0.
    # So the max of segment 1 is indeed a[p_0].
    # Similarly for other segments.
    # For the last segment [p_{k-1}+1, n-1], the max is max(a[p_{k-1}+1]...a[n-1]).
    # All these elements are not in top_k (since p_{k-1} is the last index in top_k).
    # So they are all <= the smallest value in top_k.
    # But wait, the profit of the last segment is max of that range. It might be smaller than a[p_{k-1}].
    # However, the problem asks to maximize the SUM of profits.
    # Our construction guarantees that the k largest values are each the maximum of one of the k segments.
    # Specifically, segment i (for i < k) has max = top_k[i].
    # What about the last segment? Its max is some value X.
    # Is X one of the top_k? No, because all top_k elements are at indices <= p_{k-1}, and the last segment starts at p_{k-1}+1.
    # So the last segment's max is NOT one of the top_k values.
    # This means the sum of profits is sum(top_k[0]...top_k[k-2]) + max(last_segment).
    # But we need the sum to be sum(top_k).
    # This implies that the last segment MUST contain the k-th largest element as its maximum.
    # My previous indexing was slightly off.
    # Let's re-evaluate the construction.
    # We have k segments. We want the maximums of these segments to be exactly the k largest values of the array.
    # Let the k largest values be v_1, v_2, ..., v_k (sorted by value descending, but we care about their positions).
    # Let their positions be pos_1, pos_2, ..., pos_k.
    # We can sort these positions: idx_0 < idx_1 < ... < idx_{k-1}.
    # We can define the segments as:
    # Segment 1: [0, idx_0] -> Max is a[idx_0] (which is one of the top k).
    # Segment 2: [idx_0 + 1, idx_1] -> Max is a[idx_1].
    # ...
    # Segment k: [idx_{k-2} + 1, idx_{k-1}] -> Max is a[idx_{k-1}].
    # But this only uses k-1 segments. We need k segments.
    # And we have problems after idx_{k-1}.
    # The remaining problems must be included in one of the segments.
    # If we append the remaining problems to the last segment, the max of the last segment becomes max(a[idx_{k-1}], max(remaining)).
    # Since a[idx_{k-1}] is one of the top k, and all remaining are <= a[idx_{k-1}] (because a[idx_{k-1}] is the k-th largest, and remaining are not in top k), the max remains a[idx_{k-1}].
    # So the profit of the last segment is still a[idx_{k-1}].
    # So the total profit is sum(a[idx_0]...a[idx_{k-1}]), which is the sum of the k largest values.
    # This works perfectly.
    # The segments are:
    # 1. 0 to idx_0
    # 2. idx_0+1 to idx_1
    # ...
    # k-1. idx_{k-2}+1 to idx_{k-1}
    # k. idx_{k-1}+1 to n-1 (if idx_{k-1} < n-1, otherwise this segment is empty? No, we must solve at least one problem per day. But idx_{k-1} is the index of the k-th largest. If k=n, then idx_{k-1}=n-1, and the last segment would be empty. But the problem says k <= n. If k=n, each segment has 1 problem.
    # Let's trace k=n.
    # top_k has n elements. Indices 0, 1, ..., n-1.
    # Segments:
    # 1. 0 to 0
    # 2. 1 to 1
    # ...
    # n. n-1 to n-1?
    # My logic above produced k-1 segments explicitly and then one last one.
    # Let's refine the loop.
    # We have indices idx_0, idx_1, ..., idx_{k-1}.
    # We can create k segments by splitting at these indices.
    # Segment 1 ends at idx_0.
    # Segment 2 ends at idx_1.
    # ...
    # Segment k ends at idx_{k-1}? No, that would mean the last segment ends at idx_{k-1}, leaving problems after idx_{k-1} unassigned.
    # Correct logic:
    # We need k segments. We have k "anchor" points (the indices of the k largest values).
    # Let the sorted indices be p_0, p_1, ..., p_{k-1}.
    # We can set the end of segment 1 to be p_0.
    # End of segment 2 to be p_1.
    # ...
    # End of segment k-1 to be p_{k-2}.
    # End of segment k to be n-1.
    # But we need to ensure that the max of segment k is p_{k-1}.
    # So segment k must start before or at p_{k-1} and end after or at p_{k-1}.
    # If we set segment k to start at p_{k-2} + 1 and end at n-1, then it includes p_{k-1}.
    # And since p_{k-1} is the largest in that range (as established before), the max is a[p_{k-1}].
    # So the segments are:
    # [0, p_0], [p_0+1, p_1], ..., [p_{k-2}+1, n-1].
    # This gives k segments.
    # Lengths:
    # t_1 = p_0 - 0 + 1
    # t_2 = p_1 - p_0
    # ...
    # t_{k-1} = p_{k-2} - p_{k-3} (wait, indices)
    # Let's list them clearly.
    # p = sorted indices of top k.
    # Segment 1: 0 to p[0] -> len = p[0] + 1
    # Segment 2: p[0]+1 to p[1] -> len = p[1] - p[0]
    # ...
    # Segment i: p[i-2]+1 to p[i-1] -> len = p[i-1] - p[i-2] (for i from 2 to k-1)
    # Segment k: p[k-2]+1 to n-1 -> len = (n-1) - p[k-2]
    # Wait, this uses p[0]...p[k-2] to define the first k-1 segments. The last segment uses p[k-2] as the start boundary.
    # Does the last segment contain p[k-1]?
    # Start of last segment is p[k-2] + 1.
    # End is n-1.
    # Since p[k-1] > p[k-2], p[k-1] is in [p[k-2]+1, n-1].
    # So yes, the last segment contains p[k-1].
    # And as argued, its max is a[p[k-1]].
    # So the profits are a[p[0]], a[p[1]], ..., a[p[k-1]].
    # Sum is correct.
    # What if k=1?
    # p = [p_0].
    # Loop for segments 2 to k-1 doesn't run.
    # Segment 1: 0 to p[0]? No, if k=1, we need 1 segment from 0 to n-1.
    # My formula: Segment 1: 0 to p[0]. Segment k (which is 1): p[-1]+1 to n-1?
    # Let's handle k=1 separately or adjust the logic.
    # If k=1, we just output n. Profit is max(a).
    # My logic with p=[p_0]:
    # If I follow the pattern:
    # Segments: [0, p[0]], [p[0]+1, n-1] -> 2 segments. Wrong.
    # So for k=1, the only segment is [0, n-1].
    # The "anchor" p[0] is just inside.
    # Actually, if k=1, we don't need to split at p[0]. We just take the whole array.
    # The max is max(a). Since p[0] is the index of the max element, max(a) = a[p[0]].
    # So the profit is correct.
    # But the partition is wrong if I force a split.
    # So, special case k=1: print max(a), print n.
    # For k > 1:
    # p = sorted indices of top k.
    # t = []
    # current_start = 0
    # for i in range(k-1):
    #     end = p[i]
    #     t.append(end - current_start + 1)
    #     current_start = end + 1
    # t.append(n - current_start)
    # This creates k segments.
    # Segment 1: 0 to p[0]
    # Segment 2: p[0]+1 to p[1]
    # ...
    # Segment k-1: p[k-3]+1 to p[k-2]
    # Segment k: p[k-2]+1 to n-1
    # Does this cover all?
    # Indices used: p[0], p[1], ..., p[k-2].
    # p[k-1] is in the last segment.
    # Is the max of segment k a[p[k-1]]?
    # Segment k range: [p[k-2]+1, n-1].
    # Contains p[k-1] because p[k-1] > p[k-2].
    # Max of this range is a[p[k-1]] because p[k-1] is the largest value in the entire array among the top k, and all other values in this range are not in top k (so <= a[p[k-1]]).
    # Yes.
    # So the logic holds for k > 1.
    
    if k == 1:
        print(max(a))
        print(n)
        return

    # Find indices of the k largest elements
    # We need to handle duplicates correctly. Sorting (value, index) descending works.
    indexed_a = [(a[i], i) for i in range(n)]
    indexed_a.sort(key=lambda x: x[0], reverse=True)
    
    top_k_indices = [x[1] for x in indexed_a[:k]]
    top_k_indices.sort() # Sort by index
    
    # Construct partition
    t = []
    current_start = 0
    # We use the first k-1 indices to define the first k-1 segments
    for i in range(k-1):
        end = top_k_indices[i]
        length = end - current_start + 1
        t.append(length)
        current_start = end + 1
    
    # Last segment
    last_length = n - current_start
    t.append(last_length)
    
    print(total_profit)
    print(*(t))

if __name__ == '__main__':
    solve()