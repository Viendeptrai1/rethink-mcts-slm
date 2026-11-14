import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

MOD = 10**9 + 7

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n_bin = input_data[0]
    k = int(input_data[1])
    
    n_len = len(n_bin)
    
    # Precompute the number of operations to reach 1 for any integer x
    # Since x <= n and n has up to 1000 bits, the maximum popcount is 1000.
    # However, the operation reduces x to popcount(x).
    # The maximum possible value after one operation is 1000.
    # We only need to compute operations for numbers up to 1000.
    # Let's compute ops[x] = number of steps to reach 1.
    
    # ops[x] definition:
    # if x == 1: 0 steps
    # else: 1 + ops[popcount(x)]
    
    MAX_VAL = 1005  # Slightly more than 1000
    ops = [0] * MAX_VAL
    
    # Base case
    ops[1] = 0
    
    # Compute for 2 to MAX_VAL-1
    for x in range(2, MAX_VAL):
        # Count set bits
        pc = bin(x).count('1')
        ops[x] = 1 + ops[pc]
    
    # If k == 0, the only special number is 1 (since it takes 0 steps to reach 1).
    # But the problem says "positive integer x". 1 is positive.
    # If k=0, we count numbers <= n that take 0 steps to reach 1. Only 1 fits.
    # However, note the example: k=2, numbers 3,5,6. 
    # 3 -> 2 (1 step) -> 1 (2 steps). Total 2.
    # So if k=0, answer is 1 if n >= 1 else 0. Since n >= 1 always, answer is 1.
    # But wait, the problem says "minimum number of operations ... is k".
    # If k=0, only 1 works.
    
    if k == 0:
        # Only number 1 is special.
        # Since n >= 1 (binary representation without leading zeros, so at least "1"),
        # the answer is 1.
        print(1)
        return

    # If k=1, we need numbers that reduce to 1 in 1 step.
    # That means popcount(x) must be 1.
    # Numbers with popcount 1 are powers of 2: 1, 2, 4, 8, ...
    # But wait, 1 takes 0 steps. So for k=1, we need popcount(x) such that ops[popcount(x)] == 0.
    # ops[y] == 0 implies y == 1.
    # So popcount(x) must be 1.
    # But x=1 has popcount 1, and ops[1]=0. So 1 takes 0 steps, not 1.
    # Therefore, for k=1, we need x such that popcount(x) = y and ops[y] = 0 => y=1.
    # But if popcount(x)=1, then x could be 1, 2, 4, 8...
    # For x=1: popcount=1 -> ops[1]=0. Total steps = 0. Not 1.
    # For x=2: popcount=1 -> ops[1]=0. Total steps = 1 + 0 = 1. Special.
    # For x=4: popcount=1 -> ops[1]=0. Total steps = 1. Special.
    # So for k=1, we need popcount(x) = 1 AND x != 1.
    # Actually, the recurrence is: steps(x) = 1 + steps(popcount(x)).
    # We want steps(x) = k.
    # So we need steps(popcount(x)) = k-1.
    # Let y = popcount(x). We need ops[y] == k-1.
    # Then any x with popcount(x) = y will have steps(x) = 1 + (k-1) = k.
    # Exception: if k=1, we need ops[y] = 0 => y=1.
    # Then steps(x) = 1 + 0 = 1. This works for any x with popcount 1, EXCEPT if x=1?
    # Let's re-evaluate x=1.
    # steps(1): 1 is already 1. Steps = 0.
    # Formula: if x==1, steps=0. Else 1+steps(popcount(x)).
    # So for x=1, steps=0.
    # For x=2 (10_2), popcount=1. steps(2) = 1 + steps(1) = 1 + 0 = 1.
    # So if k=1, we need x such that steps(x)=1.
    # This requires x != 1 and popcount(x) = 1.
    # So for k=1, we count numbers <= n with popcount 1, excluding 1.
    
    # General logic:
    # We need to count x in [1, n] such that steps(x) == k.
    # steps(x) depends on popcount(x).
    # Let y = popcount(x).
    # If x == 1: steps = 0.
    # If x > 1: steps = 1 + ops[y].
    # So:
    # Case 1: k == 0. Only x=1 works. Count = 1 (if n >= 1).
    # Case 2: k == 1. We need x > 1 and ops[y] == 0 => y=1.
    #          So count numbers with popcount 1, excluding 1.
    # Case 3: k > 1. We need ops[y] == k-1.
    #          Then any x with popcount y (and x > 1, but if y>=1 and x has popcount y, x>1 unless y=1 and x=1? 
    #          Wait, if y=1, x could be 1, 2, 4, 8...
    #          If x=1, steps=0. If x=2, steps=1+ops[1]=1.
    #          So if k > 1, then steps(x) = 1 + ops[y] >= 1 + 0 = 1.
    #          Since k > 1, x cannot be 1 anyway.
    #          So for k > 1, we just need ops[y] == k-1.
    #          And we count all x in [1, n] with popcount y.
    #          Note: if y=1, x=1 gives steps=0, but we are looking for steps=k>1, so x=1 is not counted.
    #          Our condition ops[y] == k-1 ensures that if we pick x with popcount y, steps(x) = 1 + (k-1) = k.
    #          This holds for x > 1. What if x=1? popcount(1)=1. ops[1]=0.
    #          If k-1 = 0 => k=1, then x=1 would satisfy ops[y]=0, but steps(1)=0 != 1.
    #          So for k=1, we must exclude x=1.
    #          For k > 1, ops[y] = k-1 >= 1, so y cannot be 1 (since ops[1]=0).
    #          Thus for k > 1, y >= 2, so x cannot be 1.
    
    # Strategy:
    # 1. Identify all y in [1, 1000] such that ops[y] == k-1.
    #    (If k=0, handled separately. If k=1, we look for y with ops[y]==0 => y=1).
    # 2. For each such y, count numbers x in [1, n] with popcount(x) == y.
    # 3. If k == 1, subtract 1 from the total count (to exclude x=1, which has popcount 1 but steps 0).
    #    Actually, if k=1, y=1. The count of numbers with popcount 1 includes 1.
    #    We need to exclude 1. So subtract 1.
    #    If k > 1, y cannot be 1 (since ops[1]=0 != k-1 for k>1), so no need to subtract.
    
    # Step 1: Find valid y
    valid_y = []
    if k == 0:
        # Handled above, but for completeness in logic:
        # We need ops[y] == -1? No, special case.
        pass
    elif k == 1:
        # Need ops[y] == 0 => y=1
        valid_y = [1]
    else:
        # Need ops[y] == k-1
        target = k - 1
        for y in range(1, 1001):
            if ops[y] == target:
                valid_y.append(y)
    
    if not valid_y:
        print(0)
        return
    
    # Step 2: Count numbers <= n with popcount == y for each y in valid_y
    # We use digit DP / combinatorics on the binary string n_bin.
    # n_bin is a string of '0' and '1'.
    # We want to count x in [1, n] with popcount == y.
    # Since n can be very large (1000 bits), we cannot iterate.
    # We use the standard technique: iterate through the bits of n from left to right.
    # Maintain a count of set bits in the prefix that matches n so far.
    # When we place a '0' where n has '1', the remaining bits can be anything (0 or 1).
    # When we place a '1' where n has '0', we exceed n, so stop.
    # When we place the same bit as n, continue.
    
    # Precompute binomial coefficients C(n, k) modulo MOD.
    # Max n is 1000.
    MAX_N = 1005
    C = [[0] * MAX_N for _ in range(MAX_N)]
    for i in range(MAX_N):
        C[i][0] = 1
        for j in range(1, i+1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD
            
    def count_with_popcount(limit_str, target_pop):
        # Count numbers in [1, limit_str] (binary) with exactly target_pop set bits.
        # limit_str is binary string.
        n = len(limit_str)
        if target_pop > n:
            return 0
        
        total = 0
        current_pop = 0
        
        for i, bit in enumerate(limit_str):
            # bit is '0' or '1'
            # We are at position i (from left, 0-indexed).
            # Remaining positions: n - 1 - i
            
            if bit == '1':
                # Option 1: Place '0' at this position.
                # Then we have (n - 1 - i) remaining bits.
                # We need to choose (target_pop - current_pop) bits from the remaining.
                needed = target_pop - current_pop
                if needed >= 0 and needed <= (n - 1 - i):
                    total = (total + C[n - 1 - i][needed]) % MOD
                
                # Option 2: Place '1' at this position (match limit_str).
                current_pop += 1
            else:
                # bit is '0'. We must place '0' to stay <= limit.
                # current_pop remains same.
                pass
        
        # After the loop, we have counted all numbers strictly less than limit_str that match the prefix logic.
        # We also need to check if limit_str itself has popcount == target_pop.
        if current_pop == target_pop:
            total = (total + 1) % MOD
            
        # The count includes 0? 
        # Our logic: 
        # When we place '0' at the first position (if limit starts with '1'), we count numbers starting with 0.
        # But numbers starting with 0 are effectively shorter numbers.
        # However, our combinatorial approach counts bit patterns of length n.
        # A pattern starting with '0' is a number with fewer than n bits.
        # Does this include 0? 
        # If target_pop == 0, then we count the number 0 (all zeros).
        # But the problem asks for positive integers.
        # So if target_pop == 0, we should subtract 1 (for the number 0).
        # But target_pop comes from valid_y, and y >= 1 (since ops[y] is defined for y>=1, and we only consider y>=1).
        # So target_pop >= 1. Thus 0 is never counted (since 0 has popcount 0).
        # So we are safe.
        
        return total

    ans = 0
    for y in valid_y:
        cnt = count_with_popcount(n_bin, y)
        ans = (ans + cnt) % MOD
    
    # If k == 1, we included x=1 (popcount 1) in the count, but steps(1)=0 != 1.
    # So we must subtract 1.
    if k == 1:
        ans = (ans - 1 + MOD) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()