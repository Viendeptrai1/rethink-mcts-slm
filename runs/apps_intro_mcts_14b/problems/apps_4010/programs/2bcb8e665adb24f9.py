import sys

def is_palindrome(subseq):
    return subseq == subseq[::-1]

def has_palindromic_subsequence(a):
    n = len(a)
    for i in range(n):
        for j in range(i + 2, n):
            for k in range(j + 1, n):
                subseq = [a[i], a[j], a[k]]
                if is_palindrome(subseq):
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
        
        if has_palindromic_subsequence(a):
            results.append("YES")
        else:
            results.append("NO")
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()