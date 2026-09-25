import sys

def construct_string(n, k, t):
    if k == 1:
        return t
    
    # Find the longest prefix of t which is also a suffix
    lps = [0] * n
    for i in range(1, n):
        j = lps[i - 1]
        while j > 0 and t[i] != t[j]:
            j = lps[j - 1]
        if t[i] == t[j]:
            j += 1
        lps[i] = j
    
    # The overlap length between consecutive occurrences of t
    overlap = lps[-1]
    
    # Construct the string s
    s = t
    for _ in range(1, k):
        s += t[overlap:]
    
    return s

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    t = data[2]
    
    result = construct_string(n, k, t)
    print(result)

if __name__ == "__main__":
    main()