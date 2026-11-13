import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = []
    for i in range(n):
        a.append(int(data[2 + i]))
    
    # Find the k largest elements in the array
    # Since we need to partition the array into k contiguous segments,
    # the maximum profit is achieved by taking the k largest values as the maximums of each segment.
    # We can sort the array to find the k largest values, but we must ensure they can form k segments.
    # Actually, the optimal strategy is: the total profit is the sum of the k largest elements in the array.
    # Why? Because each segment's profit is its max. If we have k segments, we get k max values.
    # To maximize the sum, we want the k largest possible values to be the max of their respective segments.
    # Since we can always arrange the cuts such that the k largest elements are each the maximum of their segment
    # (by cutting immediately before and after each of these large elements, ensuring no larger element is in the same segment),
    # the answer is simply the sum of the k largest elements.
    
    # However, we also need to output the partition sizes.
    # Strategy:
    # 1. Identify the k largest values. Let the k-th largest value be 'threshold'.
    # 2. We will form k segments. The first k-1 segments will each contain exactly one of the k largest values
    #    and no value larger than that specific large value (which is guaranteed if we pick the largest available).
    #    Actually, a simpler constructive approach:
    #    - Sort the array to find the k largest values. Let the sorted unique values of the top k be considered.
    #    - But duplicates matter.
    #    - Let's just pick the k largest indices. Sort these indices.
    #    - These indices will be the "pivot" elements for each of the k days.
    #    - We can make the first day end at the first pivot index.
    #    - The second day starts after the first pivot and ends at the second pivot index.
    #    - ...
    #    - The last day starts after the (k-1)-th pivot and goes to the end.
    #    - This ensures that each day's segment has at least one of the k largest values, and since we process in order,
    #      the max of each segment will be at least that value. Could it be higher?
    #      If there is a value larger than the intended max for a segment, that value would have been one of the k largest.
    #      Since we selected the k largest globally, any value larger than the k-th largest is included in our set of pivots.
    #      Therefore, within a segment defined by two consecutive pivots (or start/end), there cannot be a value larger than the pivot
    #      that belongs to a *different* segment, because that larger value would be one of the pivots and thus define a boundary.
    #      Wait, what if there are duplicates?
    #      Example: [10, 10, 10], k=2. Largest two are 10, 10. Indices 0, 1, 2. Pick first two: 0, 1.
    #      Segment 1: indices 0 to 0 -> [10], max=10.
    #      Segment 2: indices 1 to 2 -> [10, 10], max=10. Total=20. Correct.
    #      What if we picked indices 0 and 2?
    #      Segment 1: 0 to 0 -> [10].
    #      Segment 2: 1 to 2 -> [10, 10]. Max is 10. Total 20.
    #      The logic holds: The sum of the k largest elements is the maximum possible profit.
    #      To construct the solution:
    #      1. Find the k largest values. If there are ties, we just need to pick k indices corresponding to the largest values.
    #      2. Sort these k indices.
    #      3. The first segment ends at index p[0].
    #      4. The second segment ends at index p[1].
    #      5. ...
    #      6. The k-th segment ends at index p[k-1] (which is the last element n-1? Not necessarily, but we can extend the last segment to the end).
    #         Actually, the last segment must go to n-1. The pivots define the "anchor" maximums.
    #         We can define the cut points as:
    #         Cut 1: after p[0]
    #         Cut 2: after p[1]
    #         ...
    #         Cut k-1: after p[k-2]
    #         The last segment goes from p[k-2]+1 to n-1? No.
    #         Let's refine:
    #         We have k segments. We need k-1 cut positions.
    #         We select k indices that correspond to the k largest values. Let these sorted indices be idx_0, idx_1, ..., idx_{k-1}.
    #         We can set the end of segment 1 to be idx_0.
    #         End of segment 2 to be idx_1.
    #         ...
    #         End of segment k-1 to be idx_{k-2}.
    #         End of segment k to be n-1.
    #         Does this work?
    #         Segment 1: [0, idx_0]. Max is at least a[idx_0]. Since a[idx_0] is one of the k largest, and any element larger than it would be in the set of k largest,
    #         if there is a larger element in [0, idx_0], it must be one of the pivots. But idx_0 is the first pivot. So no pivot exists before idx_0.
    #         Thus, a[idx_0] is the maximum in [0, idx_0].
    #         Segment 2: [idx_0+1, idx_1]. Max is at least a[idx_1]. Any element larger than a[idx_1] in this range must be a pivot.
    #         The pivots in this range would be between idx_0 and idx_1. But we only have idx_1 as the next pivot. So no pivot exists strictly between idx_0 and idx_1.
    #         Thus, a[idx_1] is the maximum.
    #         ...
    #         Segment k: [idx_{k-2}+1, n-1]. Max is at least a[idx_{k-1}]. Any larger element must be a pivot. The only pivot >= idx_{k-1} is idx_{k-1} itself (since it's the last one).
    #         So a[idx_{k-1}] is the maximum.
    #         This construction works perfectly.
    
    # Step 1: Get indices of the k largest elements.
    # We can create a list of (value, original_index) and sort it descending.
    # Take the first k.
    
    indexed_a = [(a[i], i) for i in range(n)]
    # Sort by value descending
    indexed_a.sort(key=lambda x: x[0], reverse=True)
    
    # Take top k
    top_k_indices = sorted([idx for val, idx in indexed_a[:k]])
    
    # Calculate total profit
    total_profit = sum(val for val, idx in indexed_a[:k])
    
    # Construct the partition sizes
    # We have k segments.
    # Segment 1 ends at top_k_indices[0]
    # Segment 2 ends at top_k_indices[1]
    # ...
    # Segment k-1 ends at top_k_indices[k-2]
    # Segment k ends at n-1
    
    sizes = []
    prev = -1
    for i in range(k - 1):
        end_idx = top_k_indices[i]
        count = end_idx - prev
        sizes.append(count)
        prev = end_idx
    
    # Last segment
    last_end = n - 1
    count = last_end - prev
    sizes.append(count)
    
    print(total_profit)
    print(*(sizes))

if __name__ == '__main__':
    solve()