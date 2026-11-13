def find_longest_palindrome(s):
    n = len(s)
    longest_palindrome = ""
    
    for i in range(n):
        for j in range(i, n):
            prefix = s[:i]
            suffix = s[j+1:]
            candidate = s[i:j+1]
            
            if candidate == candidate[::-1] and len(candidate) > len(longest_palindrome):
                if s.startswith(prefix) and s.endswith(suffix):
                    longest_palindrome = candidate
    
    return longest_palindrome

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    for k in range(1, t + 1):
        s = data[k]
        result = find_longest_palindrome(s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()