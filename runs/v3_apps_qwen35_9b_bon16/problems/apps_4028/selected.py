import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    MOD = 1000000007
    length_s = len(s)
    length_total = 2 * n
    
    if length_s > length_total:
        print(0)
        return
    
    # Precompute KMP failure function (pi array) for s
    pi = [0] * length_s
    k = 0
    for q in range(1, length_s):
        while k > 0 and s[k] != s[q]:
            k = pi[k - 1]
        if s[k] == s[q]:
            k += 1
        pi[q] = k
    
    # DP State:
    # dp[i][j][k] = number of sequences of length i with balance j, having KMP match state k for string s.
    # i: current length (0 to length_total)
    # j: current balance (number of open minus close) (0 to n)
    # k: current KMP state (0 to length_s - 1), meaning the longest prefix of s that matches a suffix of the current sequence.
    
    # Dimensions:
    # i: 0 to 2n (max 200)
    # j: 0 to n (max 100)
    # k: 0 to length_s (max 200)
    
    # We will iterate and update. To save space, we can use two layers for i, but given constraints (200*100*200 = 4e6 states), 
    # a single 3D array is feasible in Python if optimized, but let's try to be memory efficient with rolling arrays.
    
    # Initialize DP
    # dp[j][k] stores the count for current length
    dp = [[0] * length_s for _ in range(n + 1)]
    dp[0][0] = 1
    
    # To handle the "containing s" condition, we can track if we have already found s.
    # However, the problem asks for sequences CONTAINING s.
    # We can add a dimension for 'found' (0 or 1).
    # new_dp[j][k][found]
    
    # Actually, let's restructure:
    # dp[i][j][k] = count of sequences of length i, balance j, KMP state k, that have NOT yet completed s.
    # Then the answer is (Total Regular Sequences of length 2n) - (Sequences of length 2n that do NOT contain s).
    # Or we can directly count those that contain s by adding a state 'found'.
    
    # Let's use the subtraction method as it might be simpler to implement the "not containing" part.
    # Total regular bracket sequences of length 2n is Catalan number C_n.
    # We need to subtract sequences of length 2n that are regular, do NOT contain s as a substring.
    
    # DP for "NOT containing s":
    # dp[j][k]: number of sequences with balance j and KMP state k that do not contain s.
    # We only care about sequences that haven't completed s yet.
    # If a transition would complete s (k -> length_s), we discard it.
    
    # Dimensions:
    # j: 0 to n
    # k: 0 to length_s - 1 (if k reaches length_s, we stop that path)
    
    dp = [[0] * length_s for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(length_total):
        new_dp = [[0] * length_s for _ in range(n + 1)]
        for j in range(n + 1):
            for k in range(length_s):
                count = dp[j][k]
                if count == 0:
                    continue
                
                # Try adding '('
                # New balance: j + 1
                if j + 1 <= n:
                    # KMP transition for '('
                    q = k
                    while q > 0 and s[q] != '(':
                        q = pi[q - 1]
                    if s[q] == '(':
                        q += 1
                    # If q becomes length_s, it means we found s. Since we are counting sequences that DO NOT contain s, skip.
                    if q < length_s:
                        new_dp[j + 1][q] = (new_dp[j + 1][q] + count) % MOD
                
                # Try adding ')'
                # New balance: j - 1
                if j - 1 >= 0:
                    # KMP transition for ')'
                    q = k
                    while q > 0 and s[q] != ')':
                        q = pi[q - 1]
                    if s[q] == ')':
                        q += 1
                    if q < length_s:
                        new_dp[j - 1][q] = (new_dp[j - 1][q] + count) % MOD
        
        dp = new_dp
    
    # Total regular bracket sequences of length 2n is Catalan(n)
    # Calculate Catalan number modulo MOD
    # C_n = (1/(n+1)) * binom(2n, n)
    
    def modInverse(a, m):
        return pow(a, m - 2, m)
    
    def nCr(n, r, mod):
        num = 1
        den = 1
        for i in range(r):
            num = (num * (n - i)) % mod
            den = (den * (i + 1)) % mod
        return (num * modInverse(den, mod)) % mod
    
    catalan = nCr(2 * n, n, MOD)
    catalan = (catalan * modInverse(n + 1, MOD)) % MOD
    
    # Sum up all valid states that do NOT contain s
    not_containing_sum = 0
    for j in range(n + 1):
        for k in range(length_s):
            not_containing_sum = (not_containing_sum + dp[j][k]) % MOD
    
    # But wait, the DP above ensures that we never reach state k=length_s.
    # However, we must also ensure that the sequence is a "regular bracket sequence".
    # The standard Catalan counting ensures balance is 0 at the end and never negative.
    # Our DP enforces balance >= 0 always (j >= 0) and j <= n (implicitly handled by check).
    # But does it ensure balance == 0 at the end?
    # Yes, because we only sum valid paths. However, the DP state allows any j at step 2n.
    # We need to sum only dp[0][k] at the end? 
    # No, the regular bracket sequence definition requires final balance 0.
    # So we only sum dp[0][k] for all k in 0..length_s-1.
    
    not_containing_sum = dp[0][0] # Wait, sum over all k where balance is 0?
    # Correct: sum dp[0][k] for k in 0..length_s-1
    
    not_containing_sum = 0
    for k in range(length_s):
        not_containing_sum = (not_containing_sum + dp[0][k]) % MOD
    
    ans = (catalan - not_containing_sum + MOD) % MOD
    print(ans)

if __name__ == '__main__':
    solve()