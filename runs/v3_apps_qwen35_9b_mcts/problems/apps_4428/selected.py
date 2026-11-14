import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    d = []
    for i in range(n):
        d.append(int(data[1 + i]))
    
    if n == 0:
        print(0)
        return

    left_sum = 0
    right_sum = 0
    left_idx = 0
    right_idx = n - 1
    max_sum = 0
    
    # We use two pointers: left_idx points to the last element of the first part
    # right_idx points to the first element of the third part
    # Initially, both parts are empty, so left_idx = -1 and right_idx = n
    # But we can simulate by starting with left_idx = 0 (considering d[0]) and right_idx = n-1 (considering d[n-1])
    # Actually, let's start with empty sums and expand.
    
    left_idx = 0
    right_idx = n - 1
    left_sum = 0
    right_sum = 0
    
    # We will iterate while we can still potentially form valid parts.
    # The condition is that the first part ends at some index i (0-based) and the third part starts at some index j (0-based).
    # So the first part is d[0...i], the third part is d[j...n-1].
    # We need i < j.
    
    # Let's maintain left_sum as sum(d[0]...d[left_idx]) and right_sum as sum(d[right_idx]...d[n-1])
    # Initially, both parts are empty.
    # We expand left_idx from 0 upwards and right_idx from n-1 downwards.
    
    left_idx = -1
    right_idx = n
    
    left_sum = 0
    right_sum = 0
    
    # We want to find max(left_sum) such that left_sum == right_sum and left_idx < right_idx - 1 (since there must be at least one element in between or they are adjacent)
    # Actually, the condition is just that the parts are disjoint and cover the array.
    # Part 1: indices 0 to left_idx
    # Part 2: indices left_idx+1 to right_idx-1
    # Part 3: indices right_idx to n-1
    # So we need left_idx < right_idx.
    
    # Strategy:
    # Start with left_idx = -1, right_idx = n.
    # While left_idx < right_idx - 1:
    #   If left_sum < right_sum:
    #       left_idx += 1
    #       left_sum += d[left_idx]
    #   Else if left_sum > right_sum:
    #       right_idx -= 1
    #       right_sum += d[right_idx]
    #   Else:
    #       # Sums are equal, record max_sum, then try to expand the smaller one (they are equal, so pick left to see if we can get a larger sum later)
    #       max_sum = left_sum
    #       left_idx += 1
    #       left_sum += d[left_idx]
    
    # Wait, the standard two pointer for this problem:
    # We start with left_sum = 0 (empty), right_sum = 0 (empty).
    # left pointer at 0, right pointer at n-1.
    # But we need to handle the case where we add elements.
    
    # Correct logic:
    # left_idx = 0, right_idx = n - 1
    # left_sum = 0, right_sum = 0
    # max_sum = 0
    # while left_idx <= right_idx:
    #   if left_sum <= right_sum:
    #       left_idx += 1
    #       if left_idx > right_idx: break # Cannot add more to left without overlapping or crossing
    #       left_sum += d[left_idx - 1] # Because we incremented left_idx, the new element is at left_idx-1
    #   else:
    #       right_idx -= 1
    #       if right_idx < left_idx - 1: break
    #       right_sum += d[right_idx]
    #   
    #   if left_sum == right_sum:
    #       max_sum = left_sum
    
    # Let's refine the loop condition and indices.
    # We want to consider all valid splits.
    # A split is defined by the end of part 1 (index i) and start of part 3 (index j).
    # 0 <= i < j <= n.
    # Part 1: d[0]...d[i-1] (if i=0, empty)
    # Part 3: d[j]...d[n-1] (if j=n, empty)
    # We need i < j.
    
    # Let's use two pointers:
    # l = 0 (number of elements in part 1)
    # r = n (number of elements in part 3, starting from end) -> actually let's use index of first element of part 3.
    # Let l be the index of the last element of part 1 (0 to n-1). If l = -1, part 1 is empty.
    # Let r be the index of the first element of part 3 (0 to n-1). If r = n, part 3 is empty.
    # Condition: l < r.
    
    # Initialize:
    # l = -1
    # r = n
    # sum1 = 0
    # sum3 = 0
    # max_val = 0
    
    # We want to move l and r to find equal sums.
    # If sum1 < sum3, we need to increase sum1 -> move l forward.
    # If sum1 > sum3, we need to decrease sum3 (move r backward) or increase sum1? No, if sum1 > sum3, we must increase sum3 to catch up, so move r backward.
    # If sum1 == sum3, we record max_val, then we can try to increase sum1 to see if we can find a larger equal sum later.
    
    l = -1
    r = n
    sum1 = 0
    sum3 = 0
    max_val = 0
    
    # We iterate while l < r - 1. Why? Because we need at least one element in between for part 2? 
    # No, part 2 can be empty. So l can be r - 1.
    # But we need to be able to add an element.
    # If l == r - 1, we cannot add to sum1 (would overlap with sum3 start) and cannot add to sum3 (would overlap with sum1 end).
    # So the loop should run while l < r - 1? 
    # Actually, we can just run while l < r. Inside, we check if we can add.
    
    # Let's restructure:
    # We have current l and r.
    # If sum1 < sum3: we must add to sum1. l += 1. If l == r, we stop (cannot add more).
    # If sum1 > sum3: we must add to sum3. r -= 1. If r == l, we stop.
    # If sum1 == sum3: record max_val. Then we can add to sum1 (to try and find a larger sum). l += 1. If l == r, stop.
    
    # Wait, if sum1 == sum3, should we add to sum1 or sum3?
    # If we add to sum1, sum1 becomes larger. Then we might need to add to sum3 to catch up.
    # If we add to sum3, sum3 becomes larger. Then we might need to add to sum1 to catch up.
    # It doesn't matter which one we pick first, but we must ensure we don't miss the optimal solution.
    # Standard approach: if equal, update max, then add to the left (increase sum1).
    
    # Loop condition: while l < r - 1? 
    # If l = r - 1, we have adjacent elements. We can still have a valid split with part 2 empty.
    # But we cannot add any more elements to either side without crossing.
    # So the loop should continue as long as we can potentially add an element.
    # We can add to left if l + 1 < r.
    # We can add to right if r - 1 > l.
    # So while l < r - 1 is not quite right because we might have a solution at l = r - 1.
    # Actually, the loop should run while l < r.
    # Inside the loop:
    #   if sum1 < sum3:
    #       l += 1
    #       if l == r: break # Cannot add more
    #       sum1 += d[l]
    #   elif sum1 > sum3:
    #       r -= 1
    #       if r == l: break
    #       sum3 += d[r]
    #   else: # equal
    #       max_val = sum1
    #       l += 1
    #       if l == r: break
    #       sum1 += d[l]
    
    # Let's trace with example 1: [1, 3, 1, 1, 4], n=5
    # l=-1, r=5, s1=0, s3=0
    # 1. s1==s3 -> max=0, l=0, s1=1. (l=0, r=5)
    # 2. s1(1) < s3(0)? No. s1 > s3? No. Equal? Yes. max=1, l=1, s1=1+3=4. (l=1, r=5)
    # 3. s1(4) > s3(0). r=4, s3=4. (l=1, r=4)
    # 4. s1(4) == s3(4). max=4, l=2, s1=4+1=5. (l=2, r=4)
    # 5. s1(5) > s3(4). r=3, s3=4+1=5. (l=2, r=3)
    # 6. s1(5) == s3(5). max=5, l=3, s1=5+1=6. (l=3, r=3) -> l==r, break.
    # Result 5. Correct.
    
    # Example 2: [1, 3, 2, 1, 4]
    # l=-1, r=5, s1=0, s3=0
    # 1. eq -> max=0, l=0, s1=1
    # 2. s1(1) < s3(0)? No. s1 > s3? No. eq -> max=1, l=1, s1=4
    # 3. s1(4) > s3(0). r=4, s3=4
    # 4. eq -> max=4, l=2, s1=4+2=6
    # 5. s1(6) > s3(4). r=3, s3=4+1=5
    # 6. s1(6) > s3(5). r=2, s3=5+4=9. (l=2, r=2) -> break.
    # Result 4. Correct.
    
    # Example 3: [4, 1, 2]
    # l=-1, r=3, s1=0, s3=0
    # 1. eq -> max=0, l=0, s1=4
    # 2. s1(4) > s3(0). r=2, s3=2
    # 3. s1(4) > s3(2). r=1, s3=2+1=3
    # 4. s1(4) > s3(3). r=0, s3=3+4=7. (l=0, r=0) -> break.
    # Result 0. Correct.
    
    # One edge case: what if the loop breaks before checking equality?
    # In step 6 of Ex 1, we updated l to 3, then broke. But we checked equality BEFORE updating l in the previous step?
    # In step 5: s1=5, s3=4. s1 > s3. r becomes 3, s3 becomes 5.
    # Next iteration: s1=5, s3=5. We enter the 'else' block, update max=5, then l becomes 3.
    # Then check l==r (3==3) and break.
    # So we captured the equality.
    
    # What if the optimal solution is at the very end where l and r meet?
    # The loop condition is while l < r.
    # If l == r, we break.
    # But if l == r, it means the parts are adjacent (part 2 is empty).
    # In the last step of Ex 1, we had l=2, r=3. s1=5, s3=5.
    # We entered the loop, found equality, updated max, then incremented l to 3.
    # Now l=3, r=3. Loop terminates.
    # We captured the value 5.
    
    # Is it possible that we need to check equality AFTER the loop?
    # Suppose the last valid state is l = r - 1 and s1 == s3.
    # In the loop, we process this state, update max, then try to expand.
    # If expanding causes l == r, we break.
    # So the equality at l = r - 1 is captured inside the loop.
    
    # What if the only solution is empty parts (sum=0)?
    # Initial state: l=-1, r=n. s1=0, s3=0.
    # Loop runs. Enters 'else', max=0, l=0.
    # If n=1, d=[10].
    # l=0, r=1. s1=10, s3=0.
    # s1 > s3. r=0. s3=10.
    # l=0, r=0. Break.
    # max=0. Correct.
    
    # What if n=2, d=[1, 1].
    # l=-1, r=2. s1=0, s3=0.
    # 1. eq -> max=0, l=0, s1=1.
    # 2. s1(1) > s3(0). r=1, s3=1.
    # 3. l=0, r=1. s1=1, s3=1. eq -> max=1, l=1, s1=1+1=2.
    # 4. l=1, r=1. Break.
    # Result 1. Correct ([1], [], [1]).
    
    # Implementation details:
    # Use sys.stdin.read for fast I/O.
    
    l = -1
    r = n
    s1 = 0
    s3 = 0
    max_val = 0
    
    while l < r:
        if s1 < s3:
            l += 1
            if l == r:
                break
            s1 += d[l]
        elif s1 > s3:
            r -= 1
            if r == l:
                break
            s3 += d[r]
        else:
            max_val = s1
            l += 1
            if l == r:
                break
            s1 += d[l]
            
    print(max_val)

if __name__ == '__main__':
    solve()