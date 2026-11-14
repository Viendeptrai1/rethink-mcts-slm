import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        num_test_cases = int(next(iterator))
    except StopIteration:
        return
    
    results = []
    
    for _ in range(num_test_cases):
        s = next(iterator)
        n = len(s)
        i = 0
        j = n - 1
        
        # Match characters from both ends
        while i < j and s[i] == s[j]:
            i += 1
            j -= 1
        
        # The remaining substring s[i:j+1] needs the longest palindrome inside it
        # We find the longest palindromic substring within s[i:j+1]
        # Since the total length constraint is small (sum <= 5000), O(N^2) per test case is acceptable.
        
        start = i
        end = j + 1  # exclusive end for slicing
        
        if start >= end:
            # All characters matched, the whole string is a palindrome
            results.append(s)
        else:
            # Find longest palindrome in s[start:end]
            sub_s = s[start:end]
            m = len(sub_s)
            max_len = 1
            best_center = 0
            
            # Check for odd length palindromes
            for center in range(m):
                l, r = center, center
                while l >= 0 and r < m and sub_s[l] == sub_s[r]:
                    l -= 1
                    r += 1
                length = r - l - 1
                if length > max_len:
                    max_len = length
                    best_center = (l + 1)  # start index in sub_s
            
            # Check for even length palindromes
            for center in range(m - 1):
                l, r = center, center + 1
                while l >= 0 and r < m and sub_s[l] == sub_s[r]:
                    l -= 1
                    r += 1
                length = r - l - 1
                if length > max_len:
                    max_len = length
                    best_center = (l + 1)
            
            # Extract the palindrome part
            pal_start = start + best_center
            pal_end = pal_start + max_len
            palindrome_part = s[pal_start:pal_end]
            
            # Construct the result: prefix + palindrome + suffix
            prefix = s[:start]
            suffix = s[end:]
            results.append(prefix + palindrome_part + suffix)
    
    for res in results:
        print(res)

if __name__ == "__main__":
    solve()