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
        if limit < 0:
            return 0
        
        s = str(limit)
        n = len(s)
        mod = X
        
        # dp[pos][tight][rem] = count
        # pos: current digit position (0 to n)
        # tight: boolean, true if we are restricted by the prefix of limit
        # rem: current remainder modulo X
        
        # We will use a dictionary for the DP state to save space and handle sparse states
        # State: (tight, rem) -> count
        # We process digit by digit from left to right.
        
        # Initial state: before processing any digits, we have remainder 0, and tight is True.
        # However, it's easier to think of it as:
        # At step i (processing digit at index i), we have a set of states (tight, rem) with counts.
        
        # Let's define dp[tight][rem] = number of ways to form the prefix such that:
        # - tight is the constraint status
        # - rem is the current remainder modulo X
        
        # Start with one way to have an empty prefix: remainder 0, tight=True.
        # But we need to be careful: the number cannot have leading zeros unless the number is 0 itself.
        # Since A >= 1, we don't need to count 0.
        # We will generate numbers with exactly 'n' digits (padding with leading zeros conceptually)
        # but we must ensure that if the number has fewer digits than n, it is handled correctly.
        # Actually, standard digit DP counts numbers from 0 to limit.
        # Since we want multiples of X, and 0 is a multiple of X, we need to check if 0 is included.
        # The problem says A >= 1, so 0 is never in [A, B].
        # Our digit DP will count numbers from 0 to limit. We will subtract the count for 0 if it's counted.
        # But wait, if we generate numbers with leading zeros, 00...0 is 0.
        # We need to make sure we don't count 0 if it's not in range, or handle it.
        # Since A >= 1, if our count includes 0, we should subtract 1 if 0 is a valid number formed (which it is).
        # However, the digit DP usually counts 0 as a valid number (all zeros).
        # Let's refine: we count numbers in [0, limit] that satisfy the condition.
        # Then result = count(B) - count(A-1).
        # If count includes 0, and 0 is not in [A, B] (since A>=1), then count(B) - count(A-1) will correctly exclude 0.
        # Example: A=1, B=20. count(20) includes 0? Yes. count(0) includes 0? Yes.
        # count(20) - count(0) = (multiples in 0..20) - (multiples in 0..0) = multiples in 1..20. Correct.
        
        # So we just need a function count_upto(N) that returns number of valid multiples in [0, N].
        
        # DP State: dp[tight][rem]
        # tight: 0 or 1
        # rem: 0 to X-1
        
        # Initialize
        # dp[1][0] = 1 (one way to have empty prefix, remainder 0, tight constraint active)
        # All others 0.
        
        dp = {}
        dp[(1, 0)] = 1
        
        for i in range(n):
            new_dp = {}
            digit_limit = int(s[i])
            
            for (tight, rem), count in dp.items():
                # Determine the range of digits we can place
                upper = digit_limit if tight else 9
                
                for d in range(10):
                    if d > upper:
                        break
                    if d not in allowed_digits:
                        continue
                    
                    new_tight = tight and (d == digit_limit)
                    new_rem = (rem * 10 + d) % mod
                    
                    state = (new_tight, new_rem)
                    new_dp[state] = new_dp.get(state, 0) + count
            
            dp = new_dp
        
        # Sum up all states
        total = sum(dp.values())
        
        # The DP counts numbers from 0 to limit.
        # The number 0 is represented by the sequence of all zeros.
        # Is 0 allowed? The problem says "composed only of certain allowed digits".
        # If '0' is in allowed_digits, then 0 is a valid number formed.
        # If '0' is not in allowed_digits, then 0 is not valid.
        # Our DP naturally handles this: if we try to place 0 at every position, it's only valid if 0 is in allowed_digits.
        # So if 0 is not allowed, the path of all zeros is never taken, so 0 is not counted.
        # If 0 is allowed, the path of all zeros is taken, so 0 is counted.
        # Since we want [A, B] and A >= 1, we don't care about 0 being counted or not, as long as it's consistent.
        # count(B) - count(A-1) will remove the contribution of 0 if it was counted in both.
        # If 0 was not counted, it's fine too.
        # So we can just return total.
        
        return total

    ans = count_multiples(B) - count_multiples(A - 1)
    print(ans)

if __name__ == "__main__":
    solve()