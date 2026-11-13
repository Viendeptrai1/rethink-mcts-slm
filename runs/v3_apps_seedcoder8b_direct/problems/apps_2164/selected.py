def find_longest_palindrome(s):
    n = len(s)
    longest_palindrome = ""
    
    for i in range(n):
        # Check for odd-length palindromes centered at i
        l, r = i, i
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 > len(longest_palindrome):
                prefix = s[:l]
                suffix = s[r+1:]
                if prefix == s[:l] and suffix == s[r+1:]:
                    longest_palindrome = s[l:r+1]
            l -= 1
            r += 1
        
        # Check for even-length palindromes centered between i and i+1
        l, r = i, i + 1
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 > len(longest_palindrome):
                prefix = s[:l]
                suffix = s[r+1:]
                if prefix == s[:l] and suffix == s[r+1:]:
                    longest_palindrome = s[l:r+1]
            l -= 1
            r += 1
    
    return longest_palindrome

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    for i in range(1, t + 1):
        s = data[i]
        result = find_longest_palindrome(s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()