def max_original_length(p):
    p = str(p)
    n = len(p)
    
    # If p is a single digit, the original array can only have one element.
    if n == 1:
        return 1
    
    # Try to find the largest possible original array
    max_length = 0
    for i in range(1, n):
        left = p[:i]
        right = p[i:]
        
        # Check if left and right can form the number p
        if int(left) >= int(right):
            # Calculate the number of elements in the original array
            original_length = 1 + (n - i)
            max_length = max(max_length, original_length)
    
    return max_length

# Read input
p = input().strip()

# Calculate and print the result
result = max_original_length(p)
print(result)