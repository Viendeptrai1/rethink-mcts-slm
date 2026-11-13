import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    t = int(data[0])
    results = []
    idx = 1
    for _ in range(t):
        s = data[idx]
        idx += 1
        n = len(s)
        i = 0
        j = n - 1
        while i < j and s[i] == s[j]:
            i += 1
            j -= 1
        prefix = s[:i]
        suffix = s[j+1:]
        mid = s[i:j+1]
        mid_rev = mid[::-1]
        if mid == mid_rev:
            res = prefix + mid + suffix
        else:
            p1 = ""
            p2 = ""
            for k in range(i):
                if prefix[:k+1] == mid_rev[:k+1]:
                    p1 = prefix[:k+1]
                if suffix[:k+1] == mid[k::-1][:k+1]:
                    p2 = suffix[:k+1]
            # Actually simpler: find longest common prefix between reversed_mid and suffix
            # and longest common prefix between mid and prefix
            # But we already matched outer parts. Now we need to extend from center.
            # The center part is s[i:j+1]. We can take a prefix of this that matches a suffix of the original string's remaining part?
            # No, the structure is: t = (prefix of s) + (middle palindrome) + (suffix of s)
            # But the middle part must be a palindrome itself? No.
            # Re-read: t = a + b, a is prefix of s, b is suffix of s. t is palindrome.
            # We matched the outer matching characters. Let the matched part be P (from both ends).
            # The remaining middle part M = s[i:j+1].
            # t will be P + X + reverse(P) where X is a palindrome formed from the middle.
            # But X doesn't have to be the whole middle. X must be such that P+X+reverse(P) is a palindrome (which it is by construction if X is palindrome)
            # AND X must be formable by taking a suffix of the remaining middle part?
            # Wait, the condition is: t = a + b, a is prefix of s, b is suffix of s.
            # We found that s starts with P and ends with reverse(P).
            # So a can be P + x, and b can be y + reverse(P).
            # Then t = P + x + y + reverse(P).
            # For t to be a palindrome, x + y must be a palindrome.
            # Also, a is prefix of s => P + x is prefix of s. Since s = P + M, x must be a prefix of M.
            # b is suffix of s => y + reverse(P) is suffix of s. Since s ends with reverse(P), y must be a suffix of M.
            # So we need to find a string x (prefix of M) and y (suffix of M) such that x + y is a palindrome.
            # To maximize length, we want to maximize len(x) + len(y).
            # Note that x and y come from M. x = M[:k], y = M[-l:].
            # We need M[:k] + M[-l:] to be a palindrome.
            # Actually, simpler approach:
            # The core palindrome part must be a palindrome itself.
            # Let the core be C. Then t = P + C + reverse(P).
            # C must be a palindrome.
            # Also, C must be obtainable as: take some prefix of M, say u, and some suffix of M, say v, such that u+v = C?
            # No. t = a + b. a is prefix of s, b is suffix of s.
            # We know s = P + M + reverse(P).
            # a = P + u, where u is a prefix of M.
            # b = v + reverse(P), where v is a suffix of M.
            # t = P + u + v + reverse(P).
            # For t to be a palindrome, u + v must be a palindrome.
            # Also, u is a prefix of M, v is a suffix of M.
            # We want to maximize len(u) + len(v).
            # Let's iterate over all possible split points in M?
            # Actually, we can just find the longest palindrome that can be formed by concatenating a prefix of M and a suffix of M.
            # But note: if u and v overlap, that's fine as long as they are valid prefix/suffix.
            # However, the simplest way:
            # The middle part of t is a palindrome. Let this palindrome be Z.
            # Z must be equal to u + v where u is prefix of M and v is suffix of M.
            # But actually, we can just consider the middle part M.
            # We want to find the longest palindrome Z such that Z = u + v, u = M[:k], v = M[n-m:].
            # Wait, there is a constraint: u and v are taken from M.
            # But notice: if we take u = M[:k] and v = M[n-m:], then Z = M[:k] + M[n-m:].
            # We need Z to be a palindrome.
            # We can iterate k from 0 to len(M), and for each k, find the longest suffix v of M such that M[:k] + v is a palindrome.
            # But that might be O(N^2). Given sum of N <= 5000, O(N^2) is acceptable.
            # Algorithm:
            # 1. Match outer characters to get P and M.
            # 2. Let M = s[i:j+1].
            # 3. We want to find max len(u) + len(v) such that u = M[:k], v = M[-l:], and u+v is a palindrome.
            # 4. Iterate k from 0 to len(M).
            #    For a fixed k, u = M[:k].
            #    We need to find the longest suffix v of M such that u+v is a palindrome.
            #    Let v = M[-l:]. Then u+v = M[:k] + M[-l:].
            #    Check if this is a palindrome. If yes, update max_len.
            #    To optimize, we can iterate l from len(M) down to 0? Or just check all l?
            #    Since N is small, we can check all pairs (k, l).
            #    Total complexity O(N^3) if we check palindrome naively. O(N^2) if we check smartly.
            #    With N=5000, N^2 = 25e6, which is a bit high for Python if constant factor is large.
            #    But sum of N is 5000, so worst case one test case with N=5000.
            #    O(N^2) should pass in Python if implemented efficiently.
            #    How to check palindrome efficiently?
            #    We can precompute hashes or just use slicing (which is fast in Python).
            #    Let's try O(N^2) with slicing.
            
            best_u = ""
            best_v = ""
            m_len = len(M)
            # Iterate over all possible lengths for u (from 0 to m_len)
            for k in range(m_len + 1):
                u = M[:k]
                # We want to find longest v (suffix of M) such that u+v is palindrome.
                # v = M[-l:] for some l.
                # We can iterate l from m_len down to 0.
                # But we can stop early? No, we need the longest.
                # Actually, we can iterate l from m_len down to 0 and break at first match?
                # No, because a shorter v might allow a longer total? No, we want longest v for fixed u.
                # So for fixed u, we want max l such that u + M[-l:] is palindrome.
                # We can iterate l from m_len down to 0.
                for l in range(m_len, -1, -1):
                    v = M[-l:] if l > 0 else ""
                    if u + v == (u + v)[::-1]:
                        if len(u) + len(v) > len(best_u) + len(best_v):
                            best_u = u
                            best_v = v
                        break # Found the longest v for this u, no need to check smaller l
            
            # Construct result
            # t = P + best_u + best_v + reverse(P)
            # But wait, is it possible that best_u and best_v overlap in M?
            # Yes, if k + l > m_len. That is allowed because u is prefix of M, v is suffix of M.
            # The concatenation u+v is just string concatenation.
            # Example: M = "aba", k=2 (u="ab"), l=2 (v="ba"). u+v = "abba", palindrome.
            # This is valid.
            
            res = P + best_u + best_v + P[::-1]
            results.append(res)
    print('\n'.join(results))

if __name__ == '__main__':
    solve()