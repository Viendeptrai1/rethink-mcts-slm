def max_tandem_repeat(s, k):
    n = len(s)
    max_length = 0
    
    # Check all possible lengths of tandem repeats
    for length in range(1, n + k + 1):
        if length % 2 == 0:
            half_length = length // 2
            found = False
            for i in range(n - half_length + 1):
                if s[i:i+half_length] == s[i+half_length:i+length]:
                    found = True
                    break
            if found:
                max_length = length
                
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