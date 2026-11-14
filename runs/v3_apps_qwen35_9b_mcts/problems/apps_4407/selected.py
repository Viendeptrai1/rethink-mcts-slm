import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    n = int(next(iterator))
    q = int(next(iterator))
    
    # Count frequency of each power of 2
    # Since values are up to 2*10^9, max power is around 30 (2^30 > 10^9)
    # We'll use a dictionary or list. A list of size 32 is sufficient.
    counts = [0] * 32
    
    for _ in range(n):
        val = int(next(iterator))
        # Find exponent d such that val = 2^d
        # Since val is guaranteed to be a power of 2, we can use bit_length - 1
        d = val.bit_length() - 1
        counts[d] += 1
        
    results = []
    
    for _ in range(q):
        b = int(next(iterator))
        
        # Greedy approach from largest power to smallest
        # We need to form value b.
        # Iterate from bit 30 down to 0.
        # If the current bit is set in b, we need a coin of that value.
        # If we have it, use it. If not, we cannot form this bit directly,
        # but maybe we can form it by combining smaller coins?
        # Actually, the standard greedy strategy for powers of 2 works if we process
        # from largest to smallest and try to satisfy the current bit requirement.
        # However, if we don't have a coin for 2^k, we can't just skip it because
        # smaller coins sum up to at most 2^(k+1)-1, which is less than 2^k + ...
        # Wait, the logic is: to form a number, we should always try to use the largest
        # available coin that is <= current remaining value.
        # But since all coins are powers of 2, this simplifies.
        
        # Let's re-evaluate:
        # We have counts of 2^0, 2^1, ..., 2^30.
        # We want to form b with minimum number of coins.
        # Strategy: Iterate from the largest possible power (say 30) down to 0.
        # If the current power 2^i is <= current target b:
        #   Take as many coins of value 2^i as possible (min of count and b // 2^i).
        #   Subtract the value from b.
        #   Add the number of coins used to the total.
        # If b becomes 0, we are done.
        # If we finish and b > 0, it's impossible -> -1.
        
        # Why does this work?
        # Because 2^i is the largest unit we can use that doesn't exceed the current remainder.
        # Using a smaller coin when a larger one fits would only increase the coin count.
        # The only constraint is availability.
        
        current_b = b
        coins_used = 0
        
        # Max power needed: 2^30 is approx 1.07e9, which covers b <= 10^9
        # Actually 2^29 is 536870912, 2^30 is 1073741824.
        # So iterating from 30 down to 0 is safe.
        
        possible = True
        for i in range(30, -1, -1):
            if current_b == 0:
                break
            
            coin_val = 1 << i
            if coin_val > current_b:
                continue
            
            # How many of this coin can we use?
            num_can_use = current_b // coin_val
            num_available = counts[i]
            
            take = min(num_can_use, num_available)
            
            if take > 0:
                current_b -= take * coin_val
                coins_used += take
        
        if current_b == 0:
            results.append(str(coins_used))
        else:
            results.append("-1")
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()