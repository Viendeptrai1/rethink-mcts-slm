import sys

def solve():
    t = sys.stdin.readline().strip()
    n = len(t)
    
    # Edge case: if length is 1, it cannot be a merge of two identical messages
    # because the overlap length must be positive and less than the message length.
    # Minimum message length would be 2 (overlap 1), resulting in min total length 3? 
    # Actually, if message s has length L, and overlap is k (1 <= k < L),
    # then result length is 2L - k.
    # Min L is 2 -> min result length = 4 - 1 = 3.
    # So if n < 3, impossible. But let's rely on the loop logic.
    
    # We need to find a string s such that s + s[1:] == t or similar overlaps?
    # No, the problem says: two identical messages s are sent.
    # They merge with an overlap of length k.
    # So the resulting string t is formed by taking s, and appending s[k:] (the part after the first k chars).
    # So t = s + s[k:]
    # This implies len(t) = len(s) + (len(s) - k) = 2*len(s) - k.
    # Also, the suffix of t of length (len(s) - k) must equal the prefix of s of that length.
    # And the prefix of t of length k must equal the suffix of s of length k (which is the same as the prefix since s is repeated).
    # Essentially, t must be formed by overlapping s with itself by k characters.
    # This means t[0 : len(s)] == s and t[len(s)-k : len(s)] == s[0:k]?
    # Let's rephrase:
    # t is constructed as: s[0...k-1] + s[k...end] + s[k...end]? No.
    # Message 1: s
    # Message 2: s
    # Overlap: last k chars of msg1 match first k chars of msg2.
    # Result: s[0...len(s)-k] + s[0...len(s)-1] (which is s) appended starting at index len(s)-k.
    # So t = s + s[len(s)-k:] ? No.
    # If overlap is k, the first message provides the first len(s)-k characters.
    # The second message provides the remaining characters.
    # The last k characters of the first message are identical to the first k characters of the second.
    # So t consists of s[0 : L-k] followed by s[0 : L].
    # Wait, if overlap is k, then the suffix of length k of s matches prefix of length k of s.
    # The combined string is: s[0 : L-k] + s[0 : L] -> this would mean the second s is fully appended but the first k are skipped?
    # Yes. t = s[0 : L-k] + s.
    # Let's check: s = "abc", k=2 (overlap "bc" == "ab"? No, overlap must match).
    # Overlap k means s[-k:] == s[:k].
    # Then t = s[:-k] + s.
    # Example: s = "aba", k=2. s[:-2] = "a". s = "aba". t = "a" + "aba" = "aaba".
    # Check manually: send "aba", "aba". Overlap 2 ("ba" matches "ab"? No).
    # "ba" != "ab". So k=2 is invalid for s="aba".
    # Valid overlap requires s[-k:] == s[:k].
    # For s="abab", k=2. s[:-2]="ab", s="abab". t="ab"+"abab" = "ababab".
    # Send "abab", "abab". Overlap 2: "ab" == "ab". Result "ababab". Correct.
    
    # So the algorithm is:
    # Iterate over all possible lengths of s, say L.
    # L can range from 1 to n.
    # However, we know len(t) = 2*L - k, where 1 <= k < L.
    # So len(t) = L + (L-k). Since k >= 1, L-k <= L-1.
    # Thus len(t) <= 2L - 1 => 2L >= n+1 => L >= ceil((n+1)/2).
    # Also k < L => L-k >= 1.
    # And k >= 1.
    # So for a fixed L, k = 2*L - n.
    # We must have 1 <= k < L.
    # 1 <= 2L - n < L
    # From 2L - n >= 1 => 2L >= n+1 => L >= (n+1)/2.
    # From 2L - n < L => L < n.
    # So L must be in range [ceil((n+1)/2), n-1].
    
    # For each such L:
    # Calculate k = 2*L - n.
    # Check if s = t[0:L] satisfies:
    # 1. s[-k:] == s[:k] (The overlap condition)
    # 2. t == s[:-k] + s (Reconstruction condition)
    # Note: If t == s[:-k] + s is true, and s[-k:] == s[:k], then the second part of the concatenation
    # s[:-k] + s will naturally have the overlap property built-in?
    # Let's verify: t = s[:-k] + s.
    # The boundary is at index len(s)-k.
    # The suffix of s[:-k] is s[-k:].
    # The prefix of s is s[:k].
    # For the merge to be valid, these must be equal.
    # So we just need to check if s[-k:] == s[:k].
    # And we assume t is formed exactly this way.
    
    found = False
    ans_s = ""
    
    for L in range((n + 1) // 2, n):
        k = 2 * L - n
        
        if k <= 0 or k >= L:
            continue
            
        s = t[:L]
        
        # Check overlap condition
        if s[-k:] == s[:k]:
            # Check reconstruction
            reconstructed = s[:-k] + s
            if reconstructed == t:
                print("YES")
                print(s)
                found = True
                break
    
    if not found:
        print("NO")

if __name__ == "__main__":
    solve()