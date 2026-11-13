import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    num_test_cases = int(data[0])
    results = []
    
    idx = 1
    for _ in range(num_test_cases):
        s = data[idx]
        idx += 1
        
        left = 0
        right = len(s) - 1
        
        while left < right and s[left] == s[right]:
            left += 1
            right -= 1
        
        prefix = s[:left]
        suffix = s[right+1:]
        
        combined = prefix + suffix
        t = combined
        
        # Find the longest palindrome in t
        # Since t is formed by matching outer characters of s, the middle part
        # (from index left to right inclusive in original s) is the core we need to check.
        # Actually, t = prefix + suffix. We need the longest palindrome within t.
        # But note: the problem asks for a palindrome t = a + b where a is prefix of s, b is suffix of s.
        # Our construction: take the longest common prefix-suffix match from ends.
        # The remaining middle part of s (s[left:right+1]) is not necessarily a palindrome.
        # However, any palindrome formed by a + b must have the property that the non-overlapping
        # prefix a and suffix b match character by character until they diverge or one ends.
        # The optimal strategy is:
        # 1. Match characters from both ends of s as much as possible -> forms the outer shell.
        # 2. The remaining substring in the middle (s[left:right+1]) needs to be reduced to its longest palindromic substring.
        # Why? Because the total string will be (matched_prefix) + (palindrome_from_middle) + (matched_suffix).
        # Wait, the condition is t = a + b, a is prefix of s, b is suffix of s.
        # Let matched_len be the number of matching characters from ends.
        # Then a = s[:left] + a_mid, b = b_mid + s[right+1:].
        # But actually, simpler logic:
        # The resulting palindrome t must start with some prefix of s and end with some suffix of s.
        # The characters at the very beginning of t and very end of t MUST match.
        # So we greedily match s[i] == s[n-1-i] from outside in. Let these matchings form the outer layers of t.
        # Once they stop matching (or we hit the same character), we are left with a middle segment s[left:right+1].
        # We must pick a palindrome from this middle segment to insert between the matched prefix and suffix.
        # Why? Because if we picked non-palindromic parts from the middle, the whole string wouldn't be a palindrome.
        # And since a must be a prefix and b a suffix, the structure is fixed:
        # t = s[0...L-1] + P + s[R+1...end] where P is a palindrome from s[L...R].
        # To maximize length, P must be the longest palindromic substring of s[left:right+1].
        
        middle = s[left:right+1]
        
        if not middle:
            results.append(t)
            continue
            
        n_mid = len(middle)
        # Find longest palindromic substring in middle
        # Since sum of lengths is small (5000), O(N^2) is acceptable.
        max_len = 1
        start = 0
        
        for i in range(n_mid):
            # Odd length palindromes
            l, r = i, i
            while l >= 0 and r < n_mid and middle[l] == middle[r]:
                if r - l + 1 > max_len:
                    max_len = r - l + 1
                    start = l
                l -= 1
                r += 1
            
            # Even length palindromes
            l, r = i, i + 1
            while l >= 0 and r < n_mid and middle[l] == middle[r]:
                if r - l + 1 > max_len:
                    max_len = r - l + 1
                    start = l
                l -= 1
                r += 1
        
        p = middle[start:start+max_len]
        results.append(prefix + p + suffix)

    print('\n'.join(results))

if __name__ == '__main__':
    solve()