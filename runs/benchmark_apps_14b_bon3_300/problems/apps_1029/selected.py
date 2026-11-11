import sys

def max_elements(p):
    p_str = str(p)
    n = len(p_str)
    
    # If p has less than 2 digits, it can only be formed from a single element
    if n < 2:
        return 1
    
    # Initialize dp array where dp[i] represents the max number of elements
    # that can form the prefix of length i
    dp = [0] * (n + 1)
    dp[0] = 1  # Base case: empty prefix can be formed by 0 elements
    
    # Iterate over each possible prefix length
    for i in range(1, n + 1):
        # Check each possible split point j
        for j in range(i):
            # Extract the two parts
            part1 = p_str[j:i]
            part2 = p_str[i:]
            
            # Check if part1 is greater than or equal to part2
            if part1 >= part2:
                # Update dp[i] considering the concatenation of part1 and part2
                dp[i] = max(dp[i], dp[j] + 1)
    
    return dp[n]

# Read input from standard input
p = int(sys.stdin.read().strip())
print(max_elements(p))