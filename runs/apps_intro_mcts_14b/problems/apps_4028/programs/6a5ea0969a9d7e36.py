import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_regular_sequences(n, s):
    # Precompute the number of ways to form balanced sequences of length 2k
    dp = [0] * (2 * n + 1)
    dp[0] = 1
    for i in range(1, 2 * n + 1):
        if i % 2 == 0:
            dp[i] = (dp[i - 2] * (i // 2)) % MOD
    
    # Function to compute the number of ways to balance a sequence with a given balance
    def ways_to_balance(balance, length):
        if balance < 0 or balance > length:
            return 0
        return dp[length] // (dp[balance] * dp[length - balance])
    
    # Calculate the number of valid sequences containing s as a substring
    total_ways = 0
    for start in range(2 * n - len(s) + 1):
        left_balance = 0
        right_balance = 0
        valid = True
        
        # Check the balance of the left part
        for i in range(start):
            if s[i] == '(':
                left_balance += 1
            else:
                left_balance -= 1
            if left_balance < 0:
                valid = False
                break
        
        if not valid:
            continue
        
        # Check the balance of the right part
        for i in range(start + len(s), 2 * n):
            if s[i] == '(':
                right_balance += 1
            else:
                right_balance -= 1
            if right_balance < 0:
                valid = False
                break
        
        if not valid:
            continue
        
        # Calculate the number of ways to balance the left and right parts
        left_length = start
        right_length = 2 * n - start - len(s)
        total_ways = (total_ways + ways_to_balance(left_balance, left_length) * ways_to_balance(right_balance, right_length)) % MOD
    
    return total_ways

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = count_regular_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()