import sys

def solve():
    t = sys.stdin.readline().strip()
    n = len(t)
    
    # We are looking for a string s such that when two copies of s are sent,
    # they overlap by some length k (1 <= k < len(s)) to form t.
    # This means: s + s[k:] == t
    # Also, len(s) must be greater than k, and k must be at least 1.
    # From the equation: len(t) = len(s) + len(s) - k = 2*len(s) - k
    # So, len(s) = (n + k) / 2.
    # Since len(s) must be an integer, (n + k) must be even.
    # Also, we must have k < len(s) => k < (n+k)/2 => 2k < n + k => k < n.
    # And k >= 1.
    
    # Let's iterate over possible overlap lengths k.
    # k can range from 1 to n-1.
    # But we also know that len(s) = (n+k)/2.
    # Let L = len(s). Then L = (n+k)/2 => k = 2L - n.
    # Constraints on k: 1 <= k < L.
    # Substitute k: 1 <= 2L - n < L
    # From 2L - n >= 1 => 2L >= n + 1 => L >= (n+1)/2
    # From 2L - n < L => L < n
    # So L ranges from ceil((n+1)/2) to n-1.
    
    # For each possible length L of s:
    #   Calculate k = 2*L - n
    #   If k < 1, skip.
    #   Check if the prefix of t of length L is equal to s.
    #   Check if s + s[k:] equals t.
    #   If yes, we found our answer.
    
    for L in range((n + 1) // 2, n):
        k = 2 * L - n
        if k < 1:
            continue
        
        # Candidate s is the prefix of t of length L
        s = t[:L]
        
        # Check if s + s[k:] == t
        # s[k:] is the part of s starting from index k
        reconstructed = s + s[k:]
        
        if reconstructed == t:
            print("YES")
            print(s)
            return

    print("NO")

if __name__ == "__main__":
    solve()