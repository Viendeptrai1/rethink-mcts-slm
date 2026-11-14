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
    
    # We need to find the minimum number of insertions.
    # This is equivalent to finding the maximum number of elements we can KEEP 
    # such that no subsegment of the kept elements sums to 0, and the gaps between 
    # kept elements are filled with separators (insertions).
    # Actually, a simpler view: we process the array and maintain a set of prefix sums.
    # If we encounter a prefix sum that has been seen before, it means the subsegment 
    # between the previous occurrence and now sums to 0. To break this, we must insert 
    # a separator somewhere. The optimal greedy strategy is:
    # When a conflict (repeated prefix sum) is detected, we "cut" the current segment 
    # by effectively resetting our prefix sum tracking. The cost is 1 insertion per cut.
    # However, we can do better by realizing that if we have a conflict, we can choose 
    # to break the segment at the point that allows us to continue as long as possible.
    # 
    # Let's reframe: We want to select a subsequence of indices i_1, i_2, ..., i_k such that
    # the original array elements at these indices, when concatenated, have no zero-sum subsegment.
    # The number of insertions will be (n - k). We want to maximize k.
    # 
    # Algorithm:
    # Iterate through the array, maintaining a set of prefix sums seen in the current "valid" block.
    # Let current_prefix_sum be the sum of elements in the current block.
    # Let seen_prefix_sums be a set of prefix sums relative to the start of the current block.
    # Initially, current_prefix_sum = 0, seen_prefix_sums = {0}.
    # 
    # For each element x in a:
    #   new_sum = current_prefix_sum + x
    #   If new_sum is in seen_prefix_sums:
    #     We have a zero-sum subsegment ending here. We must break the current block.
    #     The break happens BEFORE this element x.
    #     So, we start a new block. The new block starts with x.
    #     Reset: current_prefix_sum = 0, seen_prefix_sums = {0}.
    #     Add x to the new block: current_prefix_sum = x, seen_prefix_sums = {0, x}.
    #     Increment insertion count by 1.
    #   Else:
    #     Add new_sum to seen_prefix_sums.
    #     Update current_prefix_sum = new_sum.
    #
    # Wait, is this greedy optimal?
    # Consider: 1, -1, 1, -1.
    # i=0, x=1: sum=1, seen={0,1}
    # i=1, x=-1: sum=0 -> conflict. Break before -1. Insertions=1. New block starts with -1.
    #          sum=-1, seen={0,-1}
    # i=2, x=1: sum=0 -> conflict. Break before 1. Insertions=2. New block starts with 1.
    #          sum=1, seen={0,1}
    # i=3, x=-1: sum=0 -> conflict. Break before -1. Insertions=3.
    # Total insertions = 3.
    # But we could keep: 1, (break), -1, (break), 1, (break), -1? No, that's 3 breaks.
    # Can we do better? 
    # Original: 1, -1, 1, -1.
    # Subsegments summing to 0: [1, -1], [-1, 1], [1, -1], [1, -1, 1, -1], etc.
    # If we insert between 1 and -1: 1, X, -1, 1, -1.
    # Now subsegments: [1, -1] (indices 2,3) is still 0.
    # We need to break every contiguous zero-sum segment.
    # The greedy strategy of "break immediately upon conflict" works because any zero-sum segment 
    # ending at index i must be broken. Breaking it at the very end (before i) is valid and 
    # allows us to potentially extend the next segment further than breaking earlier? 
    # Actually, breaking earlier might merge with previous segments? No, because we reset the prefix sum set.
    # The key insight is that if we have a zero-sum segment from L to R, we MUST insert something in (L, R].
    # To maximize the kept elements, we should push the insertion as far right as possible? 
    # No, if we push it right, we might include more elements in the current block that could form a zero sum later?
    # Actually, the standard solution for this problem (Codeforces 1141C? No, similar to "Zero Sum Segments") 
    # is exactly this greedy: maintain prefix sums. If a prefix sum repeats, it means the segment between 
    # the two occurrences sums to 0. We must cut. The optimal cut is right before the current element, 
    # effectively discarding the current element as the start of a new segment (and counting 1 insertion).
    # Why is this optimal? Because if we don't cut before the current element, the zero-sum segment remains.
    # If we cut earlier, we lose more elements from the current potential block. Cutting as late as possible 
    # (i.e., just before the element that completes the zero sum) maximizes the length of the current block.
    
    insertions = 0
    current_sum = 0
    seen = {0}
    
    for x in a:
        current_sum += x
        if current_sum in seen:
            # Conflict found: subsegment sums to 0.
            # We must insert a separator.
            # The separator goes before the current element x.
            # The current block ends before x.
            # Start a new block with x.
            insertions += 1
            current_sum = x
            seen = {0, x}
        else:
            seen.add(current_sum)
            
    print(insertions)

if __name__ == '__main__':
    solve()