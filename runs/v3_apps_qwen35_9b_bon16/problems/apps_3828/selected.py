import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    p = [int(x) for x in input_data[1:]]
    
    # We need to find the longest contiguous subsequence of values such that
    # they appear in the train in the correct relative order and consecutively in value.
    # Specifically, we are looking for the longest sequence of values [x, x+1, x+2, ..., x+k-1]
    # that appear in the array `p` as a contiguous subarray in that exact order.
    # The cars not part of this longest sequence need to be moved.
    # The answer is n - length_of_longest_sequence.
    
    # Create a map from value to its index in the array for O(1) lookup
    pos = [0] * (n + 1)
    for i in range(n):
        pos[p[i]] = i
    
    max_len = 0
    current_len = 0
    
    # We iterate through values 1 to n. If value v appears immediately after v-1 in the array,
    # we extend our current contiguous segment of sorted values.
    # The base case is value 1.
    
    # Check for the longest chain starting at 1
    i = 1
    while i <= n:
        # Try to extend the chain starting at i
        # We look for the sequence: i, i+1, i+2, ...
        # They must be contiguous in the array p.
        
        # Let's start a chain at value i
        start_idx = pos[i]
        current_val = i
        current_len = 0
        
        # While the next value (current_val + 1) exists and is right after current_val in the array
        while current_val + 1 <= n and pos[current_val + 1] == start_idx + 1:
            current_val += 1
            current_len += 1
        
        if current_len > max_len:
            max_len = current_len
            
        # Move to the next potential start
        i += 1
        
        # Optimization: if current_len is 0, we just move to next. 
        # But we must check every number as a potential start of a chain.
        # Actually, the logic above checks every start from 1 to n, which is O(N^2) in worst case?
        # No, because once a chain breaks, we don't re-scan the broken part efficiently if we restart blindly.
        # Let's restructure to be O(N).
    
    # O(N) Approach:
    # Iterate through the array p. We want to find the longest subarray p[l...r] such that
    # p[k] = p[l] + (k - l) for all k in [l, r].
    # This means p[k] - k = p[l] - l = constant.
    # So we can compute diff = p[i] - i for each i.
    # We need the longest contiguous subarray where diff is constant AND the values are consecutive integers.
    # Wait, p[k] = p[l] + k - l implies p[k] - k = p[l] - l.
    # So yes, we just need the longest contiguous subarray where (p[i] - i) is constant.
    # However, we also need the values to be distinct (given) and within range 1..n (given).
    # Is that sufficient?
    # Example: 4 1 2 5 3
    # i: 0, p[i]: 4, diff: 4-0 = 4
    # i: 1, p[i]: 1, diff: 1-1 = 0
    # i: 2, p[i]: 2, diff: 2-2 = 0
    # i: 3, p[i]: 5, diff: 5-3 = 2
    # i: 4, p[i]: 3, diff: 3-4 = -1
    # Consecutive diffs: [0, 0] at indices 1,2. Length 2.
    # Answer: 5 - 2 = 3? But example says 2.
    # Wait, the example note says: "teleport the 4-th car, and then the 5-th car".
    # Original: 4 1 2 5 3
    # Move 4 to front? No, 4 is at front. Move 4 to end? -> 1 2 5 3 4.
    # Then move 5 to end? -> 1 2 3 4 5.
    # So we kept 1, 2, 3? But 1, 2, 3 are not contiguous in the original array.
    # 1 is at index 1, 2 is at index 2, 3 is at index 4. Not contiguous.
    
    # Re-reading the problem carefully: "teleport it either to the beginning ... or to the end".
    # We want to minimize moves. This is equivalent to maximizing the number of cars we DO NOT move.
    # The cars we do not move must form a contiguous subsegment in the final sorted train?
    # No. The cars we do not move must remain in their relative positions.
    # In the final sorted train 1, 2, 3, 4, 5, if we don't move a set of cars, they must appear in the final array
    # in increasing order and consecutively in terms of indices?
    # Actually, if we have a subsequence of cars that we never touch, they will end up in the middle of the final train
    # only if they are consecutive in value and their relative order is preserved.
    # But can there be gaps?
    # Suppose we keep 1, 2, 5. We move 4 and 3.
    # We can move 4 to end: 1 2 5 3. Then move 3 to end: 1 2 5 4? No.
    # The operations allow inserting at beginning or end.
    # If we keep a subsequence, say values {v1, v2, ..., vk} with v1 < v2 < ... < vk,
    # and they appear in the original array in that relative order.
    # Can we form the sorted array by moving the others?
    # Yes, if we move all smaller values to the beginning (in correct order) and all larger values to the end.
    # BUT, the values we keep must be contiguous in value range?
    # Suppose we keep 2 and 5 from 1 2 3 4 5.
    # We move 1 to front: 1 2 3 4 5. We moved 3, 4, 5? No, 5 was kept.
    # If we keep 2 and 5.
    # Original: 1 2 3 4 5.
    # Move 1 to front: 1 2 3 4 5 (2 and 5 still in relative order).
    # Move 3 to end: 1 2 4 5 3.
    # Move 4 to end: 1 2 5 3 4.
    # Move 3 to end: 1 2 5 4 3? No.
    # It seems the kept cars must form a contiguous block of values?
    # Let's check the example 4 1 2 5 3 -> answer 2.
    # Kept cars: 1, 2, 3?
    # Original indices: 1@1, 2@2, 3@4. Not contiguous indices.
    # Values: 1, 2, 3. Contiguous values.
    # If we keep 1, 2, 3.
    # We move 4 (at index 0) to end -> 1 2 5 3 4.
    # We move 5 (at index 3) to end -> 1 2 3 4 5.
    # Works.
    # So the condition is: Find the longest subsequence of values that are consecutive integers (x, x+1, x+2...)
    # that appear in the array in the correct relative order (i.e., index of x < index of x+1 < index of x+2...).
    # They do NOT need to be contiguous in the array indices.
    # Why? Because any car NOT in this set can be moved to the front or back without disturbing the relative order of the kept set.
    # If we keep x, x+1, ..., x+k-1 appearing in that order.
    # We can move all values < x to the front (in decreasing order of their original positions? No, we can just pick them up one by one).
    # Actually, we can move all values < x to the front. Since we can pick any car and put it at the front, we can arrange 1..x-1 at the front in order x-1, x-2, ...?
    # No, we need 1, 2, ..., x-1.
    # Strategy:
    # 1. Identify the set of kept cars: a contiguous range of values [L, R] such that L, L+1, ..., R appear in the array in increasing order of indices.
    # 2. Move all cars with value < L to the front. Since we can pick any car, we can pick 1, put at front. Then pick 2, put at front? No, that would make 2 1.
    # We need to put them in order 1, 2, ..., L-1.
    # We can pick L-1 and put at front. Then L-2 and put at front? Result: L-2, L-1. Not good.
    # We need to pick 1, put at front. Then 2, put at front? No.
    # Correct strategy for prefix: Pick L-1 and move to front? No.
    # Let's simulate: Target 1 2 ... L-1 [L ... R] ...
    # We have the array. We want to extract L...R and leave them in place.
    # All others must be moved.
    # Can we always move the others to form the correct sorted sequence?
    # If we have a gap in the kept sequence, say we keep 2 and 4.
    # Can we fix 3? 3 must be moved.
    # If we move 3 to the correct spot? We can only move to beginning or end.
    # So 3 must be moved to beginning or end.
    # If we move 3 to beginning, it becomes 3 ... 2 ... 4. Not sorted.
    # If we move 3 to end, it becomes ... 2 ... 4 3. Not sorted.
    # Therefore, the kept cars MUST form a contiguous range of values.
    # Because if there is a gap (e.g., keep 2 and 4, miss 3), then 3 must be moved to either start or end.
    # But 3 cannot be placed between 2 and 4 using only start/end moves if 2 and 4 are already fixed and separated by other non-moved cars?
    # Actually, if 2 and 4 are not adjacent in the final array, we can't insert between them.
    # The only way to insert 3 between 2 and 4 is if they are adjacent in the final array.
    # Since we only move to ends, the relative order of non-moved cars is preserved, and they form a contiguous block in the final array.
    # Thus, the non-moved cars must be a contiguous block of values [L, R].
    # So the problem reduces to: Find the longest subsequence of values v, v+1, v+2, ..., v+k-1 such that their indices in the input array are strictly increasing.
    # Note: They do NOT need to be contiguous in the input array indices. Just the order must be correct.
    
    # Let's re-verify with Example 1: 4 1 2 5 3
    # Values: 1, 2, 3, 4, 5.
    # Indices: 1@1, 2@2, 3@4, 4@0, 5@3. (1-based index for clarity: 1 at 2nd, 2 at 3rd, etc.)
    # Let's use 0-based:
    # 4 at 0
    # 1 at 1
    # 2 at 2
    # 5 at 3
    # 3 at 4
    #
    # Check sequence 1, 2, 3:
    # Index of 1: 1
    # Index of 2: 2 (1 < 2, OK)
    # Index of 3: 4 (2 < 4, OK)
    # Length 3.
    #
    # Check sequence 4, 5:
    # Index of 4: 0
    # Index of 5: 3 (0 < 3, OK)
    # Length 2.
    #
    # Max length is 3 (1,2,3).
    # Moves = 5 - 3 = 2. Matches example output.
    #
    # Example 2: 4 1 3 2
    # Indices: 4@0, 1@1, 3@2, 2@3.
    # Sequence 1, 2:
    # 1@1, 2@3. 1<3. OK. Length 2.
    # Sequence 3, 4:
    # 3@2, 4@0. 2>0. No.
    # Sequence 1, 2, 3?
    # 1@1, 2@3, 3@2. 3>2. No.
    # Max length 2.
    # Moves = 4 - 2 = 2. Matches example output.
    
    # Algorithm:
    # Store position of each number: pos[v] = index.
    # Iterate v from 1 to n-1. Check if pos[v+1] > pos[v].
    # If yes, extend current streak. If no, reset streak to 1.
    # Keep track of max streak.
    
    pos = [0] * (n + 1)
    for i in range(n):
        pos[p[i]] = i
        
    max_len = 0
    current_len = 0
    
    # Start from 1. The first element of any valid sequence must be some v.
    # We can iterate v from 1 to n.
    # If v is the start of a sequence, current_len = 1.
    # Then check v+1, v+2...
    
    # Actually, simpler:
    # Iterate v from 1 to n-1.
    # If pos[v+1] > pos[v], then we can extend the sequence ending at v.
    # But we don't know where it started.
    # We just need the longest chain.
    # Let dp[v] = length of consecutive sequence ending at v.
    # dp[v] = dp[v-1] + 1 if pos[v] > pos[v-1] else 1.
    # Then max(dp) is the answer.
    
    # Base case: dp[1] = 1.
    # Then for v = 2 to n:
    #   if pos[v] > pos[v-1]: dp[v] = dp[v-1] + 1
    #   else: dp[v] = 1
    # max_len = max(max_len, dp[v])
    
    if n == 0:
        print(0)
        return

    # pos array is 1-indexed for values 1..n
    # pos[v] is the index in p
    
    current_len = 1
    max_len = 1
    
    for v in range(2, n + 1):
        if pos[v] > pos[v-1]:
            current_len += 1
        else:
            current_len = 1
        if current_len > max_len:
            max_len = current_len
            
    print(n - max_len)

if __name__ == '__main__':
    solve()