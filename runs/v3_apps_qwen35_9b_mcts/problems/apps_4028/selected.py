import sys

# Increase recursion depth just in case, though we will use iterative DP
sys.setrecursionlimit(20000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]
    m = len(s)
    MOD = 1000000007

    # Precompute KMP failure function (pi array)
    pi = [0] * m
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j

    # Precompute transition table for KMP automaton
    # trans[state][char] -> next_state
    # state ranges from 0 to m-1 (m is absorbing state for full match)
    # char: 0 for '(', 1 for ')'
    trans = [[0] * 2 for _ in range(m + 1)]
    
    for state in range(m + 1):
        for char_code in range(2):
            char = '(' if char_code == 0 else ')'
            if state == m:
                # If we already matched s, we stay in state m
                trans[state][char_code] = m
                continue
            
            # Try to extend the match
            j = state
            while j > 0 and char != s[j]:
                j = pi[j-1]
            if char == s[j]:
                j += 1
            trans[state][char_code] = j

    # DP state: dp[i][j][k]
    # i: number of characters placed so far (0 to 2n)
    # j: current balance (number of open - number of closed) (0 to n)
    # k: current KMP state (0 to m)
    # We only need two layers for i to save space, but given n=100, 2n=200, m=200,
    # a full 3D array of size 201*101*201 is about 4 million integers, which is fine (~16MB).
    
    # Initialize DP
    # dp[j][k] will store the count for current step i
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # Start with 0 chars, balance 0, KMP state 0

    # Iterate over positions from 1 to 2n
    for i in range(1, 2 * n + 1):
        new_dp = [[0] * (m + 1) for _ in range(n + 1)]
        
        # Iterate over all possible previous states
        for bal in range(n + 1):
            for state in range(m + 1):
                count = dp[bal][state]
                if count == 0:
                    continue
                
                # Try adding '('
                # New balance: bal + 1
                if bal + 1 <= n:
                    next_state = trans[state][0]
                    # If we reached full match (state m), we stay there
                    if next_state == m:
                        next_state = m
                    new_dp[bal + 1][next_state] = (new_dp[bal + 1][next_state] + count) % MOD
                
                # Try adding ')'
                # New balance: bal - 1
                if bal - 1 >= 0:
                    next_state = trans[state][1]
                    if next_state == m:
                        next_state = m
                    new_dp[bal - 1][next_state] = (new_dp[bal - 1][next_state] + count) % MOD
        
        dp = new_dp

    # Sum up all states where we have a full match (state m) and balance is 0
    ans = 0
    for state in range(m + 1):
        if state == m:
            ans = (ans + dp[0][state]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()