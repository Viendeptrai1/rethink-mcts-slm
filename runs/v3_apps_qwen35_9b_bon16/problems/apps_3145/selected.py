import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    X = int(input_data[0])
    A = int(input_data[1])
    B = int(input_data[2])
    allowed_str = input_data[3]
    allowed_digits = set(allowed_str)

    def count_multiples(limit):
        if limit < 1:
            return 0
        digits = [int(c) for c in allowed_str]
        digits.sort()
        n = len(digits)
        
        # Precompute powers of 10 to avoid repeated multiplication
        pow10 = [1] * 20
        for i in range(1, 20):
            pow10[i] = pow10[i-1] * 10
        
        # DP state: (position, remainder, is_less, is_started)
        # position: current digit index from left (0 to 18, since 10^18 > 10^11)
        # remainder: current number % X
        # is_less: boolean, true if we are strictly less than limit prefix
        # is_started: boolean, true if we have started placing non-zero digits
        
        # We will use memoization with a tuple key
        from functools import lru_cache
        
        limit_str = str(limit)
        L = len(limit_str)
        
        # We need to handle numbers up to limit. Since limit < 10^11, L <= 11.
        # However, to be safe and generic, we can go up to 18 digits.
        # But for optimization, we only go up to len(limit_str).
        # Actually, numbers with fewer digits than limit are automatically "less".
        # So we can sum up counts for lengths 1 to len(limit_str)-1, then handle len(limit_str) with is_less constraint.
        
        # Let's define a helper that counts valid numbers with exactly 'length' digits that are <= some prefix logic?
        # Better approach: Standard digit DP that counts valid numbers <= limit.
        # State: (pos, rem, tight, started)
        # pos: 0 to L-1
        # rem: 0 to X-1
        # tight: bool
        # started: bool
        
        @lru_cache(None)
        def dp(pos, rem, tight, started):
            if pos == L:
                if started and rem == 0:
                    return 1
                return 0
            
            limit_digit = int(limit_str[pos]) if tight else 9
            res = 0
            
            # Determine range of digits to try
            start_digit = 0 if started else 0 # If not started, we can put 0 and stay not started, or put >0 and start
            # Actually if not started, we can place 0 and remain not started, or place allowed digit >0 and start.
            # But we must ensure we don't count the number 0 unless limit >= 0 and we want to include it.
            # The problem says multiples between A and B, A>=1, so 0 is never included.
            # So if not started, placing 0 keeps us not started.
            
            for d in digits:
                if d > limit_digit:
                    break
                
                new_tight = tight and (d == limit_digit)
                new_started = started or (d != 0)
                
                # If we are not started and place 0, we continue with not started
                # If we place non-zero, we start
                
                # Calculate new remainder
                if new_started:
                    new_rem = (rem * 10 + d) % X
                else:
                    # Still not started, remainder doesn't change (conceptually 0)
                    new_rem = rem
                
                res += dp(pos + 1, new_rem, new_tight, new_started)
            
            return res

        # Run DP
        return dp(0, 0, True, False)

    ans = count_multiples(B) - count_multiples(A - 1)
    print(ans)

if __name__ == '__main__':
    solve()