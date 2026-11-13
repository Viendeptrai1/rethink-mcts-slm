import sys

def solve():
    t = sys.stdin.readline().strip()
    n = len(t)
    
    # We are looking for a string s such that s + s[overlap:] == t
    # where overlap is the suffix of s that matches the prefix of s.
    # Let k be the length of the overlap (1 <= k < len(s)).
    # Then s has length L, and t has length 2*L - k.
    # Also, s = t[0:L] and s must equal t[0:L] which implies t[0:L] == t[k:L+k] == ...
    # Actually, the condition is:
    # t = s + s[k:]
    # This means t[0:L] = s and t[L-k:] = s[k:]
    # So t[0:L] must equal t[k:L+k] ? No.
    # t = s + s[k:]
    # Let L = len(s). Then len(t) = L + (L - k) = 2L - k.
    # So k = 2L - n.
    # Constraints on k:
    # 1. k >= 1 (positive overlap)
    # 2. k < L (overlap length less than message length)
    # From k = 2L - n, we have L = (n + k) / 2.
    # Since L must be integer, n + k must be even.
    # Also k < L => k < (n+k)/2 => 2k < n + k => k < n.
    # And k >= 1.
    # So we can iterate over possible values of k from 1 to n-1.
    # For a fixed k:
    #   L = (n + k) / 2
    #   If (n + k) is odd, skip.
    #   Check if k < L.
    #   Construct candidate s = t[0:L].
    #   Check if t == s + s[k:].
    #   If yes, print YES and s, then exit.
    
    for k in range(1, n):
        if (n + k) % 2 != 0:
            continue
        L = (n + k) // 2
        if k >= L:
            continue
        
        s = t[:L]
        # Check if t is formed by s + s[k:]
        reconstructed = s + s[k:]
        if reconstructed == t:
            print("YES")
            print(s)
            return

    print("NO")

if __name__ == "__main__":
    solve()