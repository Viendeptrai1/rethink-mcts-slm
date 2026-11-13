import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n_bin = input_data[0]
    k = int(input_data[1])
    m = len(n_bin)
    
    MOD = 10**9 + 7
    
    # Precompute popcount for numbers up to 60 (since n < 2^1000, but we only care about the popcount of numbers <= n)
    # The maximum possible popcount for a number <= n is bounded by the number of bits in n, which is at most 1000.
    # However, the operation reduces x to popcount(x). The next number is at most ~60 for x < 2^60, but here x can be up to 2^1000.
    # But note: the first operation reduces x (which can be up to 2^1000) to popcount(x) which is at most 1000.
    # Then subsequent operations are on numbers <= 1000.
    # So we need to compute the chain length for numbers up to 1000.
    
    MAX_VAL = 1005
    ops = [0] * MAX_VAL
    
    def get_ops(x):
        if x == 1:
            return 0
        count = 0
        while x != 1:
            x = bin(x).count('1')
            count += 1
        return count

    for i in range(2, MAX_VAL):
        ops[i] = get_ops(i)
    
    # If k is 0, then we need numbers that reduce to 1 in 0 operations -> only 1 itself.
    # If k is 1, we need numbers that reduce to 1 in 1 operation -> numbers with popcount(x) = 1 and x != 1.
    # Generally, we need popcount(x) = y such that ops[y] = k-1.
    
    # Special case: if k=0, only number 1 is special.
    if k == 0:
        if n_bin == '1':
            print(1)
        else:
            print(0)
        return

    # If k=1, we need popcount(x) = 1 and x != 1.
    # If k > 1, we need popcount(x) = y where ops[y] == k-1.
    
    target_popcounts = []
    for y in range(1, MAX_VAL):
        if ops[y] == k - 1:
            target_popcounts.append(y)
    
    # Also, we must exclude the case where the number itself is 1 if k > 0 (since 1 reduces to 1 in 0 ops, not k).
    # But our logic of popcount chain handles this: 
    # If we require popcount(x) = y, and y=1, then ops[y]=0. So if k-1=0 => k=1, then y=1 is included.
    # But we must exclude x=1 because for x=1, the number of operations is 0, not k.
    # However, if k=1, we want numbers that become 1 in 1 op. x=1 becomes 1 in 0 ops, so x=1 is NOT special for k=1.
    # Our set of target_popcounts for k=1 includes y=1 (since ops[1]=0).
    # So we will count numbers with popcount=1, which includes 1. We must subtract 1 if 1 is in the count.
    
    # Count numbers <= n with a specific popcount c, excluding the number 1 if c=1.
    # We use digit DP (or combinatorics) on the binary string n_bin.
    
    def count_with_popcount(c):
        # Count numbers x in [1, n] such that popcount(x) == c.
        # We can compute this by iterating through the bits of n.
        # Let's do a standard digit DP approach counting numbers < n and then handle n itself, 
        # or simply iterate bit by bit counting strictly less and then check n.
        # Actually, easier: count numbers in [0, n] with popcount c, then subtract 1 if 0 is counted (popcount 0) and adjust for 1.
        # But 0 is not positive integer? The problem says positive integer.
        # So range is [1, n].
        
        total = 0
        current_pop = 0
        n_len = len(n_bin)
        
        # We'll count numbers strictly less than n with popcount c, plus check n itself.
        # Standard approach:
        # Iterate from most significant bit.
        # If we place a 0 where n has 1, then the remaining bits can be anything, as long as total popcount is c.
        # If we place a 1 where n has 1, we continue to next bit with current_pop incremented.
        # If we place a 0 where n has 0, we continue (but this path is invalid for strictly less? No, if n has 0, we can only place 0 to match prefix, or we can't place 1 because that would exceed n).
        # Actually, the standard algorithm:
        # Iterate i from 0 to n_len-1:
        #   If n_bin[i] == '1':
        #     Option 1: Place '0' at this position. Then the remaining (n_len - 1 - i) bits can be chosen freely to reach the target popcount.
        #       We need (c - current_pop) more bits from the remaining positions.
        #       If 0 <= (c - current_pop) <= (remaining_len), add comb(remaining_len, needed).
        #     Option 2: Place '1' at this position (matches n), so current_pop increases, and we continue.
        #   If n_bin[i] == '0':
        #     We must place '0' to stay <= n (cannot place 1). So just continue.
        # After the loop, check if n itself has popcount c.
        
        # Precompute combinations
        # Since max length is 1000, we need nCr up to 1000.
        
        fact = [1] * (n_len + 1)
        inv = [1] * (n_len + 1)
        for i in range(2, n_len + 1):
            fact[i] = (fact[i-1] * i) % MOD
        
        inv[n_len] = pow(fact[n_len], MOD - 2, MOD)
        for i in range(n_len - 1, 1, -1):
            inv[i] = (inv[i+1] * (i + 1)) % MOD
            
        def nCr(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv[r] * inv[n-r]) % MOD
            return (num * den) % MOD
        
        # Count strictly less than n with popcount c
        count_less = 0
        cur_pop = 0
        for i, bit in enumerate(n_bin):
            if bit == '1':
                remaining_len = n_len - 1 - i
                needed = c - cur_pop
                if 0 <= needed <= remaining_len:
                    count_less = (count_less + nCr(remaining_len, needed)) % MOD
                cur_pop += 1
        
        # Check n itself
        if cur_pop == c:
            count_less = (count_less + 1) % MOD
            
        # The problem asks for positive integers. 0 is not included.
        # Our count includes 0 only if c=0 and we count the number 0? 
        # In our logic, we are counting numbers in [0, n] with popcount c.
        # The number 0 has popcount 0. If c=0, we counted 0. But we want positive integers.
        # However, c will be from target_popcounts. 
        # If c=0, then target_popcounts includes 0? 
        # ops[0] is not defined in our loop (started from 2). Let's fix ops for 0 and 1.
        # But logically, a positive integer x has popcount >= 1. So c=0 is impossible for positive integers.
        # So if c=0, the count should be 0.
        # Our function count_with_popcount(0) would return 1 (for 0) if n>=0.
        # So we must handle c=0 separately.
        
        if c == 0:
            return 0
            
        return count_less

    # Total answer
    ans = 0
    for c in target_popcounts:
        cnt = count_with_popcount(c)
        ans = (ans + cnt) % MOD
    
    # If k=1, we included numbers with popcount 1. This includes the number 1 (binary '1').
    # But for x=1, operations to reduce to 1 is 0, not 1. So we must subtract 1 if we counted it.
    # Did we count 1? 
    # If c=1, count_with_popcount(1) counts numbers in [1, n] with popcount 1.
    # The number 1 has popcount 1. So it is counted.
    # But 1 is not special for k=1.
    # So if k=1, we subtract 1.
    # Note: if k > 1, then c cannot be 1 because ops[1] = 0, and we need ops[c] = k-1.
    # If k > 1, then k-1 >= 1, so c must be >= 2 (since ops[1]=0). 
    # So c=1 only appears when k-1=0 => k=1.
    # So only when k=1, we have to subtract 1.
    
    if k == 1:
        ans = (ans - 1 + MOD) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()