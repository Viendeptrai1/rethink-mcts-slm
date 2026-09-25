import sys

def has_palindrome_subsequence(a):
    n = len(a)
    # Create a dictionary to store the last occurrence of each element
    last_occurrence = {}
    
    for i in range(n):
        if a[i] in last_occurrence:
            # Check for a palindrome of length 3 or more
            for j in range(last_occurrence[a[i]] + 1, i):
                if a[j] == a[i]:
                    return True
        last_occurrence[a[i]] = i
    
    return False

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        a = list(map(int, data[index:index + n]))
        index += n
        if has_palindrome_subsequence(a):
            results.append("YES")
        else:
            results.append("NO")
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()