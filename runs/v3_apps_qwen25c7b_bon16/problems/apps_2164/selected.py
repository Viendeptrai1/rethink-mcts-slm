def longest_palindrome_prefix_suffix(s):
    n = len(s)
    for i in range(n - 1, -1, -1):
        if s[:i+1] == s[:i+1][::-1]:
            return s[:i+1]
    return ""

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        s = data[index]
        result = longest_palindrome_prefix_suffix(s)
        results.append(result)
        index += 1
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()