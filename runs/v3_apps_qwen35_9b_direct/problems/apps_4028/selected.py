import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    s = input_data[1]
    m = len(s)
    MOD = 1000000007

    if m > 2 * n:
        print(0)
        return

    # Precompute KMP failure function for s
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and s[k] != s[i]:
            k = pi[k-1]
        if s[k] == s[i]:
            k += 1
        pi[i] = k

    # DP state: dp[i][j][k] = number of sequences of length i with balance j and KMP match length k
    # i: current length (0 to 2n)
    # j: current balance (0 to n)
    # k: current match length in s (0 to m-1)
    # We only care about states where k < m (if k reaches m, we have found s)
    # However, once we find s, we can stay in a "found" state. To simplify, let's use k from 0 to m,
    # where k=m means we have already found s. But to save space and avoid confusion, we can treat k=m as an absorbing state.
    # Actually, it's easier to have k from 0 to m, and if we transition to m, we stay at m.
    # But note: the problem requires s to appear at least once. So we can count total regular sequences and subtract those that never contain s?
    # Alternatively, we can have a state for "already found". Let's use k in [0, m] where k=m means found.
    # However, the KMP state for "found" is not needed beyond knowing we found it. So we can have:
    # dp[i][j][k] for k in [0, m-1] and a separate flag for found? 
    # Instead, let's let k go from 0 to m, and if k becomes m, we stay at m. But note: if we are at k=m, 
    # then any subsequent character doesn't change the fact that we have found s. So we can have a state m.
    # However, the KMP automaton for k=m is trivial: from m, on any char, we stay at m? 
    # Actually, no: the problem is that once we have found s, we don't care about the suffix anymore. 
    # So we can have a state "found" (let's call it state m) and from state m, on any character, we remain in state m.
    # But wait: the KMP automaton for a string s: if we are at state m (meaning we just matched s), 
    # then if we read a character, the new state is the longest proper suffix of (s + char) that is a prefix of s.
    # However, the problem only requires that s appears at least once. So once we have matched s, we are done with the condition.
    # Therefore, we can have a state "found" (index m) and from state m, we transition to state m on any character.
    # This is valid because we don't need to track the suffix after the first occurrence.

    # So states: k in [0, m]. k=m means we have already found s.
    # Dimensions: i in [0, 2n], j in [0, n], k in [0, m]
    # But note: j (balance) cannot exceed n, and also cannot be negative. Also, at the end, j must be 0.

    # Initialize dp table
    # dp[i][j][k]
    # We'll use a 2D array for the current i and update for i+1 to save space, but since n is small (100) and m is up to 200,
    # 2n * n * m = 200 * 100 * 200 = 4e6, which is acceptable in Python if we are careful.
    # However, 4e6 states might be a bit heavy for Python in a tight loop. We can optimize by using two layers for i.

    # Let's use dp[j][k] for the current length i.
    # Initialize: dp[0][0] = 1, others 0.

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    # We'll iterate for length from 0 to 2n-1
    for length in range(2 * n):
        new_dp = [[0] * (m + 1) for _ in range(n + 1)]
        for j in range(n + 1):
            for k in range(m + 1):
                count = dp[j][k]
                if count == 0:
                    continue
                # Try adding '('
                # New balance: j+1
                if j + 1 <= n:
                    # Compute next k state
                    if k == m:
                        nk = m
                    else:
                        # Try to extend the match
                        # We are at state k, meaning we have matched s[0:k]
                        # Now we add s[k] if it matches, but actually we are adding a character c.
                        # We need to see if s[k] == c. If yes, then new state is k+1.
                        # If not, we use the failure function to backtrack.
                        c = '('
                        while k > 0 and s[k] != c:
                            k = pi[k-1]
                        if s[k] == c:
                            nk = k + 1
                        else:
                            nk = 0
                        # But note: if nk becomes m, then we have found s.
                        if nk == m:
                            nk = m
                    new_dp[j+1][nk] = (new_dp[j+1][nk] + count) % MOD

                # Try adding ')'
                # New balance: j-1
                if j - 1 >= 0:
                    if k == m:
                        nk = m
                    else:
                        c = ')'
                        while k > 0 and s[k] != c:
                            k = pi[k-1]
                        if s[k] == c:
                            nk = k + 1
                        else:
                            nk = 0
                        if nk == m:
                            nk = m
                    new_dp[j-1][nk] = (new_dp[j-1][nk] + count) % MOD
        dp = new_dp

    # Sum up all states where k == m (found s) and balance == 0 at length 2n
    ans = dp[0][m] % MOD
    print(ans)

if __name__ == '__main__':
    solve()