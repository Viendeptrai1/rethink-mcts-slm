import sys

def has_palindrome_subsequence(a):
    n = len(a)
    # Create a dictionary to store the last occurrence of each element
    last_occurrence = {}
    for i in range(n):
        last_occurrence[a[i]] = i
    
    # Check for palindromic subsequences of length at least 3
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] == a[j]:
                # Find the last occurrence of a[i] after position j
                k = last_occurrence[a[i]]
                if k > j:
                    return True
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