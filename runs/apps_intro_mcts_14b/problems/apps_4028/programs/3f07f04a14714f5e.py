import sys

MOD = 10**9 + 7

def catalan(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(i):
            dp[i] = (dp[i] + dp[j] * dp[i - j - 1]) % MOD
    return dp

def count_sequences(n, s):
    m = len(s)
    if m > 2 * n:
        return 0
    
    # Calculate Catalan numbers up to n
    c = catalan(n)
    
    # Precompute the number of valid sequences of lengths 0 to n
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = sum(dp[j] * dp[i - j - 1] for j in range(i)) % MOD
    
    # Count the number of valid sequences containing s as a substring
    count = 0
    for start in range(2 * n - m + 1):
        left_len = start
        right_len = 2 * n - start - m
        
        # Calculate the number of valid sequences on the left and right of s
        left_count = dp[left_len // 2]
        right_count = dp[right_len // 2]
        
        # Check if the remaining part of the sequence is valid
        balance = 0
        valid = True
        for i in range(m):
            if s[i] == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                valid = False
                break
        
        if valid and balance == 0:
            count = (count + left_count * right_count) % MOD
    
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = count_sequences(n, s)
    print(result)

if __name__ == "__main__":
    main()