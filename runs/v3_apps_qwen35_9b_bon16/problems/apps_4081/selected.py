import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    # We need to find the longest strictly increasing subsequence formed by
    # repeatedly taking from the left or right end.
    
    # Since all elements are distinct (C1), we can use a greedy approach with a middle strategy.
    # Let L be the current left pointer and R be the current right pointer.
    # We maintain the last taken value 'last'.
    # At each step, we look at a[L] and a[R].
    # - If both are greater than 'last' and one is smaller than the other, pick the smaller one.
    # - If both are greater than 'last' and equal (impossible in C1), or both are smaller (impossible if we only pick valid moves), we handle accordingly.
    # - If both are greater than 'last' and equal, it's impossible in C1, so we ignore this case.
    # - If one is valid and the other is not, pick the valid one.
    # - If both are valid and equal (impossible in C1), skip.
    # - If both are invalid, stop.
    # - If both are valid and neither is smaller than the other (i.e., a[L] == a[R]), this happens only if we have elements left in the middle and both ends are the same value? No, values are distinct.
    # Wait, if a[L] == a[R], that's impossible since all values are distinct.
    # So the only ambiguity arises when:
    # 1. Both > last. Then pick min(a[L], a[R]).
    # 2. Only a[L] > last. Pick L.
    # 3. Only a[R] > last. Pick R.
    # 4. Neither > last. Stop.
    
    # BUT there is a catch: What if a[L] == a[R]? In C1, this never happens.
    # However, consider the case where we pick an element, and then later we might face a situation where picking one side forces us into a dead end while the other doesn't?
    # Actually, with distinct elements and the goal of strictly increasing, the greedy strategy of picking the smallest available valid element works.
    # Why? Because picking a larger element now might prevent us from picking a medium element later that could have extended the sequence further. Picking the smallest valid element gives us the most room for future numbers.
    
    # Let's re-verify the logic:
    # Current available: left end (l), right end (r).
    # Last taken: last_val (init -1).
    # If l < last_val or r < last_val: invalid.
    # If l > last_val and r > last_val:
    #   If l < r: pick l (because l is smaller, leaving r which is larger for potentially larger next numbers).
    #   If r < l: pick r.
    #   If l == r: impossible in C1.
    # If l > last_val and r < last_val: pick l.
    # If l < last_val and r > last_val: pick r.
    # If both < last_val: stop.
    
    # Is this always optimal?
    # Consider sequence: [10, 2, 3, 4, 5]
    # last = -1
    # l=10, r=5. Both > -1. Pick min(10, 5) = 5 (R). last=5. Seq: [5]
    # Now arr: [10, 2, 3, 4]
    # l=10, r=4. Both > 5? No, 4 < 5. 10 > 5.
    # Only l valid? No, l=10 > 5, r=4 < 5. So pick l? 
    # Wait, if I pick 5, next I have [10, 2, 3, 4]. 
    # l=10, r=4. last=5.
    # 10 > 5, 4 < 5. Only 10 is valid. Pick 10.
    # Seq: 5, 10. Done. Length 2.
    # But optimal is: pick 10 (L)? No, 10 > 5. 
    # Let's trace properly:
    # Start: [10, 2, 3, 4, 5], last=-1.
    # l=10, r=5. Both > -1. Pick 5 (R). last=5.
    # Remaining: [10, 2, 3, 4].
    # l=10, r=4. 10 > 5, 4 < 5. Only 10 valid. Pick 10 (L).
    # Remaining: [2, 3, 4].
    # l=2, r=4. Both < 5? Yes. Stop.
    # Total length 2.
    
    # Alternative:
    # Start: [10, 2, 3, 4, 5].
    # Pick 10 (L). last=10.
    # Remaining: [2, 3, 4, 5].
    # l=2, r=5. 2 < 10, 5 < 10. Stop.
    # Length 1.
    
    # Another example: [2, 1, 5, 4, 3]
    # last=-1. l=2, r=3. Both > -1. Pick 2 (L). last=2.
    # Rem: [1, 5, 4, 3]. l=1, r=3. 1 < 2, 3 > 2. Pick 3 (R). last=3.
    # Rem: [1, 5, 4]. l=1, r=4. 1 < 3, 4 > 3. Pick 4 (R). last=4.
    # Rem: [1, 5]. l=1, r=5. 1 < 4, 5 > 4. Pick 5 (R). last=5.
    # Rem: [1]. l=1, r=1. 1 < 5. Stop.
    # Path: L, R, R, R. Length 4. Correct.
    
    # What if there is a tie in validity? i.e., a[L] == a[R]?
    # In C1, values are distinct, so a[L] != a[R] as long as L != R.
    # If L == R, there is only one element left.
    # If that element > last, we take it. If not, stop.
    
    # So the algorithm:
    # l = 0, r = n-1, last = -1
    # moves = []
    # while l <= r:
    #   val_l = a[l]
    #   val_r = a[r]
    #   candidates = []
    #   if val_l > last: candidates.append(('L', val_l))
    #   if val_r > last: candidates.append(('R', val_r))
    #   if not candidates: break
    #   # Now we have 1 or 2 candidates.
    #   # Since distinct, if 2 candidates, val_l != val_r.
    #   # Sort candidates by value ascending.
    #   candidates.sort(key=lambda x: x[1])
    #   pick = candidates[0]
    #   if pick[0] == 'L':
    #     l += 1
    #   else:
    #     r -= 1
    #   last = pick[1]
    #   moves.append(pick[0])
    
    # Wait, is greedy by smallest value always correct?
    # Consider: [5, 4, 3, 2, 1]
    # last=-1. l=5, r=1. Both > -1. Pick 1 (R). last=1.
    # Rem: [5, 4, 3, 2]. l=5, r=2. 5>1, 2>1. Pick 2 (R). last=2.
    # ... Pick 3, 4, 5.
    # Path: R, R, R, R, L. Length 5. Correct.
    
    # Consider: [1, 2, 3, 4, 5]
    # last=-1. l=1, r=5. Pick 1 (L). last=1.
    # l=2, r=5. Pick 2 (L). ...
    # Path: LLLLL. Correct.
    
    # Is there a case where picking the smaller one is bad?
    # Suppose we have [10, 20, 30, 40, 5] and last=5.
    # l=10, r=5? No, array is [10, 20, 30, 40, 5].
    # l=10, r=5. last=5.
    # 10 > 5, 5 not > 5. Only 10 valid. Pick 10.
    # This seems fine.
    
    # What if: [10, 11, 12, 13, 5] and last=4.
    # l=10, r=5. Both > 4. Pick 5 (R). last=5.
    # Rem: [10, 11, 12, 13]. l=10, r=13. Both > 5. Pick 10 (L). last=10.
    # Rem: [11, 12, 13]. l=11, r=13. Pick 11 (L).
    # ... 12, 13.
    # Path: R, L, L, L. Length 5.
    # If we picked 10 first? last=10. Then 11, 12, 13 valid. 5 invalid. Length 4.
    # So picking smaller was better.
    
    # The logic holds for C1 (distinct elements).
    
    l = 0
    r = n - 1
    last = -1
    res = []
    
    while l <= r:
        v_l = a[l]
        v_r = a[r]
        
        choices = []
        if v_l > last:
            choices.append(('L', v_l))
        if v_r > last:
            choices.append(('R', v_r))
        
        if not choices:
            break
        
        # In C1, if len(choices) == 2, then v_l != v_r.
        # We pick the one with the smaller value.
        choices.sort(key=lambda x: x[1])
        
        move = choices[0][0]
        val = choices[0][1]
        
        if move == 'L':
            l += 1
        else:
            r -= 1
        
        last = val
        res.append(move)
    
    print(len(res))
    print("".join(res))

if __name__ == '__main__':
    solve()