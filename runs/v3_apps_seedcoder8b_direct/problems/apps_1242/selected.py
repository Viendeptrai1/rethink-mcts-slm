def solve():
    import sys
    input = sys.stdin.read
    s = input().strip()
    
    n = len(s)
    result = [0] * n
    
    # We will iterate over each prefix and decide whether to reverse it or not
    for i in range(n):
        # Check if reversing the prefix from 0 to i makes it lexicographically smaller
        if s[:i+1] != ''.join(sorted(s[:i+1])):
            result[i] = 1
    
    # Print the result
    print(' '.join(map(str, result)))