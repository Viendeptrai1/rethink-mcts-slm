import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    e = int(input_data[1])
    
    if e == 0:
        power_of_2 = "1"
    else:
        power_of_2 = str(1 << e)
    
    target = power_of_2
    m = len(target)
    
    if m > len(str(n)):
        print(0)
        return
    
    # Precompute digit counts for numbers with length < m (they can't contain target)
    # We only care about numbers with length >= m.
    
    # We will use digit DP.
    # State: (index in target, tight constraint, started flag)
    # But we need to count numbers that contain the substring at least once.
    # It's easier to count total numbers - numbers that do NOT contain the substring.
    
    # Let's define a function count_without(n_str, target) that returns count of numbers in [0, n] 
    # that do NOT contain target as substring.
    
    def count_without(n_str, target):
        n_len = len(n_str)
        m = len(target)
        if m > n_len:
            return n + 1
        
        # dp[i][j][tight][started]
        # i: current digit position we are placing (0 to n_len-1)
        # j: current match length in target (0 to m-1)
        # tight: boolean, are we restricted by n_str
        # started: boolean, have we started placing non-zero digits (to handle leading zeros correctly)
        # However, leading zeros are part of the number representation for the purpose of substring?
        # The problem says "decimal representation". Usually, 00125 is just 125.
        # So leading zeros do not count towards the substring match.
        # We need to track if we are still in leading zeros.
        
        # State: (pos, match_len, tight, started)
        # pos: 0..n_len
        # match_len: 0..m-1 (if match_len reaches m, we have found the target, but we are counting WITHOUT, so we stop this path)
        # tight: 0 or 1
        # started: 0 or 1
        
        # We use memoization.
        from functools import lru_cache
        
        @lru_cache(None)
        def dp(pos, match_len, tight, started):
            if match_len == m:
                return 0  # We found the target, so this path is invalid for "without"
            
            if pos == n_len:
                return 1  # Successfully placed all digits without finding target
            
            limit = int(n_str[pos]) if tight else 9
            total = 0
            
            for digit in range(limit + 1):
                new_tight = tight and (digit == limit)
                new_started = started or (digit != 0)
                
                if not new_started:
                    # Still in leading zeros, match_len remains 0
                    total += dp(pos + 1, 0, new_tight, False)
                else:
                    # We are placing a digit in the number
                    # Update match_len
                    new_match_len = match_len
                    if match_len > 0:
                        # Check if adding 'digit' extends the match
                        # We need to check if target[match_len] == digit
                        if target[match_len] == str(digit):
                            new_match_len = match_len + 1
                        else:
                            # Mismatch, need to find the longest prefix of target that is a suffix of (target[:match_len] + digit)
                            # This is KMP failure function logic.
                            # Let current string be S = target[:match_len] + digit
                            # We want the length of the longest proper prefix of target that is a suffix of S.
                            # Since m is small (up to 19 for 2^62), we can brute force this.
                            temp_s = target[:match_len] + str(digit)
                            for l in range(min(m, len(temp_s)), 0, -1):
                                if temp_s.endswith(target[:l]):
                                    new_match_len = l
                                    break
                            else:
                                new_match_len = 0
                    else:
                        # match_len is 0
                        if target[0] == str(digit):
                            new_match_len = 1
                        else:
                            new_match_len = 0
                    
                    total += dp(pos + 1, new_match_len, new_tight, True)
            
            return total

        return dp(0, 0, True, False)

    total_numbers = n + 1
    without_count = count_without(str(n), target)
    result = total_numbers - without_count
    print(result)

if __name__ == "__main__":
    solve()