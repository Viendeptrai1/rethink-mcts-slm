def find_longest_palindrome(s):
    n = len(s)
    for i in range(n, -1, -1):
        for j in range(i):
            sub = s[j:i]
            if sub == sub[::-1]:
                return sub

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    index = 1
    
    for _ in range(t):
        s = data[index]
        result = find_longest_palindrome(s)
        results.append(result)
        index += 1
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()