def max_tandem_repeat(s, k):
    n = len(s)
    max_length = 0
    
    # Check for tandem repeats starting within the original string
    for i in range(n):
        for j in range(i + 1, n // 2 + 1):
            if s[i:i+j] == s[i+j:i+2*j]:
                max_length = max(max_length, 2 * j)
    
    # Check for tandem repeats spanning the newly added characters
    for i in range(n):
        for j in range(1, min(k, n - i) + 1):
            if s[i:i+j] == s[i+j:i+2*j]:
                max_length = max(max_length, 2 * j)
    
    return max_length

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    k = int(data[1])
    result = max_tandem_repeat(s, k)
    print(result)