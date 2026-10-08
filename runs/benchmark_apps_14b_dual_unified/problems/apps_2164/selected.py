import sys

def find_longest_palindrome(s):
    n = len(s)
    max_length = 0
    best_palindrome = ""
    
    for i in range(n + 1):
        prefix = s[:i]
        reversed_prefix = prefix[::-1]
        if s.endswith(reversed_prefix) and len(prefix) > max_length:
            max_length = len(prefix)
            best_palindrome = prefix
    
    return best_palindrome

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        s = data[index]
        index += 1
        result = find_longest_palindrome(s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()