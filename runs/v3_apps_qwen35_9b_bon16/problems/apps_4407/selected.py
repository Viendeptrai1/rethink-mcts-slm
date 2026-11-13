import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    q = int(next(iterator))
    
    counts = {}
    for _ in range(n):
        val = int(next(iterator))
        exp = val.bit_length() - 1
        counts[exp] = counts.get(exp, 0) + 1
    
    results = []
    
    for _ in range(q):
        b = int(next(iterator))
        
        # Check if b is possible at all (sum of all coins < b is a quick fail, but we need exact check)
        # Actually, since we have counts per power, we can simulate greedy from largest to smallest
        # However, b can be up to 10^9, so we need to be efficient.
        
        # Strategy: Try to form b using largest coins first (greedy works for canonical coin systems like powers of 2)
        # But we are limited by the counts we have.
        
        # Let's compute total sum first to do a quick impossible check? Not strictly necessary if we simulate carefully.
        # Better: simulate greedy from highest possible bit down to 0.
        
        # Find the highest bit needed for b
        if b == 0:
            results.append(0)
            continue
        
        max_bit = b.bit_length() - 1
        
        # We only need to consider bits from max_bit down to 0
        # Also, we might need larger coins if we use them to form smaller values? 
        # No, in powers of 2, 2^k cannot help form 2^j where j < k efficiently unless we have many small coins.
        # Actually, the greedy strategy for powers of 2 is: use the largest coin <= current remainder.
        # But we must respect available counts.
        
        current_b = b
        num_coins = 0
        
        possible = True
        
        # We iterate from the highest bit that could possibly be used.
        # The highest bit we might need is around 60 (since 2^60 > 10^18, but b <= 10^9, so ~30).
        # However, we might have coins larger than b. Those are useless for forming b exactly.
        
        # Determine the range of bits to check
        # Start from max(max_bit, highest bit in our coins) down to 0? 
        # Actually, if we have a coin larger than b, we can never use it to form b (since all coins are positive).
        # So start from min(max_bit, highest available coin bit) down to 0.
        
        start_bit = max_bit
        # Ensure we don't go below 0
        if start_bit < 0:
            results.append(-1)
            continue
            
        # Optimization: if the sum of all coins < b, impossible.
        # Calculating total sum might be O(N) which is fine once, but let's avoid recomputing.
        # We can precompute total sum.
        total_sum = 0
        for exp in counts:
            total_sum += (1 << exp) * counts[exp]
            
        if total_sum < b:
            results.append(-1)
            continue
            
        # Greedy approach
        # We try to cover the bits of b from most significant to least significant.
        # However, simply checking bits of b is not enough because we might need to break down a larger coin?
        # No, we cannot break a coin. We can only combine coins.
        # So we must find a subset of available coins that sums to b.
        # For powers of 2, the greedy strategy of "take the largest coin <= current target" is optimal IF we have enough coins.
        # But with limited counts, it's slightly different.
        # Actually, the standard greedy works: iterate from highest bit down. If the bit is set in target, try to take a coin of that power.
        # If we don't have a coin of that power, can we form it from smaller coins? Yes, 2^(k-1) + 2^(k-1) = 2^k.
        # But the greedy strategy usually goes from largest to smallest.
        # Let's refine:
        # We want to represent b.
        # Iterate bit k from 60 down to 0.
        # If the k-th bit of b is 1, we MUST form 2^k using coins of power <= k.
        # The most efficient way is to use one 2^k coin. If not available, use two 2^(k-1), etc.
        # However, using smaller coins to form a larger one "consumes" them, which might be bad for lower bits.
        # Wait, is greedy optimal here?
        # Consider target = 6 (110 binary). Coins: one 4, two 2. Greedy: take 4 (rem 2), take 2 (rem 0). Count 2. Optimal.
        # Consider target = 6. Coins: three 2s. Greedy: take 2 (rem 4), take 2 (rem 2), take 2 (rem 0). Count 3. Optimal.
        # Consider target = 3. Coins: one 4. Impossible.
        # The issue is: do we ever prefer using two 2^(k-1) over one 2^k if we have a 2^k?
        # No, because using 2^k counts as 1 coin, while two 2^(k-1) count as 2 coins. Since we want to MINIMIZE coins, we should always prefer larger coins.
        # So the strategy:
        # For each bit k from high to low:
        #   If bit k is set in b:
        #     We need to cover this 2^k.
        #     Prefer using a coin of value 2^k. If available, use one, decrement count, increment ans.
        #     If not available, we MUST form this 2^k from smaller coins.
        #     But wait, if we don't have 2^k, we can try to form it from 2^(k-1)s.
        #     However, this logic is tricky because "forming 2^k from smaller" is equivalent to saying "we didn't save those smaller coins for lower bits".
        #     Actually, the correct greedy for "min coins" with powers of 2 and limited supply:
        #     Iterate k from 60 down to 0.
        #     If we have a coin 2^k, and we need to cover some amount, should we use it?
        #     Yes, always use the largest possible coin that fits the remaining amount, provided it helps minimize count.
        #     BUT, we have a constraint: we can't split coins.
        #     So, simply:
        #     current_target = b
        #     For k from 60 down to 0:
        #        coin_val = 1 << k
        #        if coin_val > current_target: continue
        #        take = min(counts.get(k, 0), current_target // coin_val)
        #        current_target -= take * coin_val
        #        num_coins += take
        #        if current_target == 0: break
        #     If current_target == 0: ans = num_coins else: -1
        
        # Is this greedy correct?
        # Example: Target 6 (110). Coins: {4:1, 2:2}.
        # k=2 (4): take min(1, 6//4=1) = 1. rem=2. ans=1.
        # k=1 (2): take min(2, 2//2=1) = 1. rem=0. ans=2. Correct.
        # Example: Target 6. Coins: {2:3}.
        # k=2: take min(0, 1) = 0. rem=6.
        # k=1: take min(3, 3) = 3. rem=0. ans=3. Correct.
        # Example: Target 12. Coins: {8:1, 4:1, 2:2}.
        # k=3 (8): take 1. rem=4. ans=1.
        # k=2 (4): take 1. rem=0. ans=2. Correct.
        # Example: Target 12. Coins: {4:3}.
        # k=3: 0.
        # k=2: take 3. rem=0. ans=3. Correct.
        # Example: Target 7 (111). Coins: {4:1, 2:2, 1:2}.
        # k=2 (4): take 1. rem=3. ans=1.
        # k=1 (2): take 1. rem=1. ans=2.
        # k=0 (1): take 1. rem=0. ans=3. Correct.
        
        # What if we have too many large coins? e.g. Target 3, Coins {4:10, 1:10}.
        # k=2 (4): 4 > 3, skip.
        # k=0 (1): take 3. ans=3. Correct.
        
        # What if we have a coin that is exactly the target?
        # Target 4, Coins {8:1, 4:1, 2:10}.
        # k=3 (8): skip.
        # k=2 (4): take 1. rem=0. ans=1. Correct.
        
        # Seems the greedy "take as many of the largest possible coin as fits" works for minimizing count.
        # Why? Because any 2^k can be replaced by two 2^(k-1). Replacing a larger coin with smaller ones increases coin count.
        # So we should maximize the use of larger coins.
        # The only constraint is we can't use a coin larger than the remainder.
        
        current_target = b
        ans = 0
        possible = True
        
        # Determine upper bound for bit iteration. 
        # Max b is 10^9 < 2^30. Max coin value 2*10^9 < 2^31.
        # So iterating from 30 down to 0 is sufficient.
        # Let's use 31 to be safe.
        
        for k in range(31, -1, -1):
            if current_target == 0:
                break
            coin_val = 1 << k
            if coin_val > current_target:
                continue
            
            avail = counts.get(k, 0)
            if avail == 0:
                continue
                
            # How many of this coin can we take?
            # We can take at most 'avail' and at most 'current_target // coin_val'
            take = min(avail, current_target // coin_val)
            
            current_target -= take * coin_val
            ans += take
        
        if current_target == 0:
            results.append(ans)
        else:
            results.append(-1)
            
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()