import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    p = [int(x) for x in input_data[1:]]
    
    # We want to find the longest contiguous subsequence of values 
    # that appear in the array in the correct relative order and consecutively.
    # Specifically, we are looking for the longest sequence of values v, v+1, v+2, ..., v+k-1
    # such that they appear in the array in that exact order (not necessarily consecutively in the array,
    # but no other elements can be between them if we want to keep them as a block to move to the end).
    # Actually, the optimal strategy is to keep a contiguous block of values [x, x+1, ..., y] 
    # that already appear in the array in the correct relative order without any gaps in their positions 
    # relative to each other? 
    # Let's re-evaluate.
    # If we decide to keep a set of cars in their current positions and move the rest, 
    # the cars we keep must form a contiguous range of values [L, R] and they must appear in the array 
    # in increasing order of their values, and importantly, there should be no other kept cars between them.
    # But since we can only move cars to the very beginning or very end, the cars we do NOT move 
    # must form a contiguous subsegment in the final sorted array. 
    # Why? Because if we don't move a car with value v, and we don't move a car with value v+1, 
    # and there is a car with value u (where u < v or u > v) that we also don't move, 
    # then in the final sorted array, u must be adjacent to v or v+1. 
    # If we don't move u, v, v+1, they must end up adjacent in the original array relative to each other?
    # Actually, the standard solution for this problem is:
    # Find the longest subsequence of the form k, k+1, k+2, ..., k+m-1 such that in the given array,
    # these numbers appear in that exact order and consecutively? 
    # No, they don't have to be consecutive in the array, but they must be consecutive in value.
    # And crucially, if we keep a set of numbers, say {3, 4, 5}, and they appear in the array as ... 3 ... 4 ... 5 ...,
    # we can move everything before 3 to the front and everything after 5 to the back.
    # However, if there is a number 2 between 3 and 4 in the array, we cannot keep 3, 4, 5 together 
    # without moving 2, because 2 would end up between 3 and 4 in the final array if we don't move it,
    # but we want 2 to be before 3. So if we don't move 2, it must be part of our kept sequence.
    # Therefore, the cars we do NOT move must form a contiguous range of values [L, R] AND they must 
    # appear in the array in increasing order of indices.
    # Wait, if we keep [L, R], then in the final array they will be at positions corresponding to L, L+1, ..., R.
    # In the original array, they must appear in increasing order of their values. 
    # But do they need to be consecutive in the original array? 
    # Suppose the array is [1, 3, 2, 4]. We want to sort it. 
    # If we keep 1 and 4, we move 3 to end -> [1, 2, 4, 3] (no), move 3 to end -> [1, 2, 4, 3] is not sorted.
    # Move 2 to end -> [1, 3, 4, 2]. Move 3 to end -> [1, 2, 3, 4]. 2 moves.
    # What if we keep 2, 3, 4? In [1, 3, 2, 4], 2 is at index 2, 3 at index 1, 4 at index 3. 
    # Order is 3, 2, 4. Not increasing. So we can't keep 2, 3, 4.
    # What if we keep 1, 2, 3? 1 at 0, 2 at 2, 3 at 1. Order 1, 3, 2. Not increasing.
    # What if we keep 1, 4? 1 at 0, 4 at 3. Increasing. We move 3, 2. 
    # Move 3 to end: [1, 2, 4, 3]. Move 2 to end: [1, 4, 3, 2] -> no.
    # Move 2 to end first: [1, 3, 4, 2]. Move 3 to end: [1, 4, 2, 3] -> no.
    # Move 3 to end: [1, 2, 4, 3]. Move 2 to end: [1, 4, 3, 2].
    # Actually, the operation is: pick a car, move to front or back.
    # To sort [1, 3, 2, 4]:
    # Move 3 to end: [1, 2, 4, 3]. Move 3 to end: [1, 2, 3, 4]. 2 moves.
    # Can we do better? Keep 1, 2, 4? No, 2 and 4 are not consecutive values.
    # The cars we keep MUST be a contiguous range of values [x, x+1, ..., y].
    # AND they must appear in the array in increasing order of their values.
    # AND there should be no "gaps" in the array that force us to move intermediate elements?
    # Actually, if we keep a set of values S, and we move everything else, the relative order of S 
    # in the original array must be the same as in the sorted array. 
    # Since the sorted array has values 1, 2, ..., n, the subset S must appear in the original array 
    # in increasing order of their values.
    # Furthermore, if we keep a set of values that are NOT contiguous (e.g., 1 and 3, but not 2), 
    # then 2 must be moved. If 2 is moved, it can go to front or back. 
    # If we keep 1 and 3, and move 2 to front: [2, 1, 3, ...]. Not sorted.
    # Move 2 to back: [..., 1, 3, 2]. Not sorted.
    # So the kept values MUST form a contiguous range of integers [L, R].
    # Additionally, in the original array, the occurrences of L, L+1, ..., R must appear in that order.
    # Is that sufficient? 
    # Example: 4 1 2 5 3. 
    # Possible contiguous ranges:
    # [1, 2]: indices 1, 2. Order 1, 2. OK. Length 2. Moves = 5-2 = 3.
    # [2, 3]: 2 at 2, 3 at 4. Order 2, 3. OK. Length 2.
    # [4, 5]: 4 at 0, 5 at 3. Order 4, 5. OK. Length 2.
    # [1, 2, 3]: 1 at 1, 2 at 2, 3 at 4. Order 1, 2, 3. OK. Length 3. Moves = 5-3 = 2.
    # [4, 5, 6]: 6 not present.
    # Max length is 3 ([1, 2, 3]). Answer 2. Matches example.
    # Example 2: 4 1 3 2.
    # [1, 2]: 1 at 1, 2 at 3. OK.
    # [2, 3]: 2 at 3, 3 at 2. Order 3, 2. Not increasing.
    # [3, 4]: 3 at 2, 4 at 0. Not increasing.
    # [1, 2, 3]: 1 at 1, 2 at 3, 3 at 2. Order 1, 3, 2. Not increasing.
    # Max length 2. Answer 2. Matches example.
    
    # Algorithm:
    # 1. Store the position of each number. pos[v] = index of v in p.
    # 2. We want to find the longest sequence L, L+1, ..., R such that pos[L] < pos[L+1] < ... < pos[R].
    # 3. This is equivalent to finding the longest contiguous subarray in the array of positions 
    #    where the values are consecutive integers.
    #    Let's create an array A where A[i] = pos[i+1] for i from 0 to n-1 (representing values 1 to n).
    #    We want the longest subarray A[i...j] such that A[i] < A[i+1] < ... < A[j].
    #    Wait, no. The condition is pos[v] < pos[v+1] < ... < pos[v+k].
    #    So we iterate v from 1 to n-1. If pos[v] < pos[v+1], we extend the current sequence.
    #    Otherwise, we break and start a new sequence at v+1.
    # 4. The maximum length of such a sequence is max_len.
    # 5. The answer is n - max_len.
    
    pos = [0] * (n + 1)
    for i in range(n):
        pos[p[i]] = i
        
    max_len = 0
    current_len = 0
    
    # Check sequences starting from 1
    # We can iterate from 1 to n-1. If pos[i] < pos[i+1], increment current_len. Else reset.
    # But we need to handle the start correctly.
    
    # Let's trace:
    # If pos[1] < pos[2], then 1,2 is a candidate. current_len becomes 2.
    # If pos[2] < pos[3], then 1,2,3 is a candidate. current_len becomes 3.
    # If pos[2] > pos[3], then the sequence breaks. The sequence 1,2 ends. 
    # The new sequence starts at 3? Yes, because 3 could be the start of a new contiguous block.
    # So if pos[i] < pos[i+1], we extend. Else, we reset current_len to 1 (starting a new sequence at i+1).
    
    # Wait, if pos[1] > pos[2], then 1,2 is not valid. The sequence starting at 1 has length 1.
    # The sequence starting at 2 has length at least 1.
    # So:
    # current_len = 1 (for value 1)
    # for i from 1 to n-1:
    #   if pos[i] < pos[i+1]:
    #       current_len += 1
    #   else:
    #       current_len = 1
    #   max_len = max(max_len, current_len)
    
    # Example 1: 4 1 2 5 3
    # pos: 1->1, 2->2, 3->4, 4->0, 5->3
    # i=1: pos[1]=1, pos[2]=2. 1<2. current_len=2. max=2.
    # i=2: pos[2]=2, pos[3]=4. 2<4. current_len=3. max=3.
    # i=3: pos[3]=4, pos[4]=0. 4>0. current_len=1. max=3.
    # i=4: pos[4]=0, pos[5]=3. 0<3. current_len=2. max=3.
    # Result 3. Ans = 5-3=2. Correct.
    
    # Example 2: 4 1 3 2
    # pos: 1->1, 2->3, 3->2, 4->0
    # i=1: pos[1]=1, pos[2]=3. 1<3. cur=2. max=2.
    # i=2: pos[2]=3, pos[3]=2. 3>2. cur=1. max=2.
    # i=3: pos[3]=2, pos[4]=0. 2>0. cur=1. max=2.
    # Result 2. Ans = 4-2=2. Correct.
    
    current_len = 1
    max_len = 1
    
    for i in range(1, n):
        if pos[i] < pos[i+1]:
            current_len += 1
        else:
            current_len = 1
        if current_len > max_len:
            max_len = current_len
            
    print(n - max_len)

if __name__ == '__main__':
    solve()