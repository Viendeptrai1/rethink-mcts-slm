import sys

def find_longest_palindrome(s):
    n = len(s)
    max_length = 0
    best_palindrome = ""
    
    # Check all possible palindromes
    for i in range(n):
        for j in range(i, n):
            candidate = s[i:j+1]
            if candidate == candidate[::-1]:
                if j - i + 1 > max_length:
                    max_length = j - i + 1
                    best_palindrome = candidate
    
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
        results.append(find_longest_palindrome(s))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()