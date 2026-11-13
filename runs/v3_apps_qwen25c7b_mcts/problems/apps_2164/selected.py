def longest_palindrome(s):
    n = len(s)
    max_len = 0
    result = ""
    
    for i in range(n):
        # Check odd-length palindromes centered at i
        left, right = i, i
        while left >= 0 and right < n and s[left] == s[right]:
            if right - left + 1 > max_len:
                max_len = right - left + 1
                result = s[left:right+1]
            left -= 1
            right += 1
        
        # Check even-length palindromes centered between i and i+1
        left, right = i, i + 1
        while left >= 0 and right < n and s[left] == s[right]:
            if right - left + 1 > max_len:
                max_len = right - left + 1
                result = s[left:right+1]
            left -= 1
            right += 1
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        s = data[index]
        index += 1
        result = longest_palindrome(s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()