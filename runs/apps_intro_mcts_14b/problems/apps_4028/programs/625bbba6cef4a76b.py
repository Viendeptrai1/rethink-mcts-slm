import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_sequences(n, s):
    # Calculate the number of ways to form a regular bracket sequence of length 2n
    def catalan(n):
        if n == 0 or n == 1:
            return 1
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1
        for i in range(2, n + 1):
            for j in range(i):
                dp[i] = (dp[i] + dp[j] * dp[i - j - 1]) % MOD
        return dp[n]

    # Calculate the number of ways to place s in a regular bracket sequence of length 2n
    def count_ways_to_place_s(n, s):
        len_s = len(s)
        if len_s > 2 * n:
            return 0
        
        # Precompute the number of valid sequences of different lengths
        catalan_numbers = [0] * (2 * n + 1)
        for i in range(2 * n + 1):
            catalan_numbers[i] = catalan(i // 2)
        
        # Count the number of valid placements
        total_ways = 0
        for start in range(2 * n - len_s + 1):
            left_part = s[:start]
            right_part = s[start + len_s:]
            
            # Check if the left part and right part can be balanced
            balance = 0
            valid_left = True
            for char in left_part:
                if char == '(':
                    balance += 1
                else:
                    balance -= 1
                if balance < 0:
                    valid_left = False
                    break
            
            balance = 0
            valid_right = True
            for char in right_part[::-1]:
                if char == ')':
                    balance += 1
                else:
                    balance -= 1
                if balance < 0:
                    valid_right = False
                    break
            
            if valid_left and valid_right:
                left_len = start
                right_len = 2 * n - len_s - start
                total_ways = (total_ways + catalan_numbers[left_len // 2] * catalan_numbers[right_len // 2]) % MOD
        
        return total_ways

    return count_ways_to_place_s(n, s)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Output the result
print(count_sequences(n, s))