def solve():
    import sys
    input = sys.stdin.read
    s = input().strip()
    
    n = len(s)
    result = [0] * n
    
    # Initialize the first prefix
    current_prefix = s[0]
    reverse_prefix = s[0][::-1]
    
    # Determine if we should reverse the first prefix
    if reverse_prefix < current_prefix:
        result[0] = 1
        current_prefix = reverse_prefix
    
    # Iterate over the string to determine the optimal prefixes to reverse
    for i in range(1, n):
        current_prefix += s[i]
        reverse_prefix = s[i] + reverse_prefix
        
        # Compare the current prefix and its reverse
        if reverse_prefix < current_prefix:
            result[i] = 1
            current_prefix = reverse_prefix
    
    # Print the result
    print(' '.join(map(str, result)))