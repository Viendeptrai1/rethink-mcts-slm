def min_instability(n, a):
    a.sort()
    # Calculate the initial instability
    initial_instability = a[-1] - a[0]
    
    # Calculate the minimum instability by removing each element
    min_instability = float('inf')
    for i in range(1, n):
        # Calculate instability if we remove the i-th element
        instability = max(a[i-1], a[-1] - a[i])
        min_instability = min(min_instability, instability)
    
    return min_instability

# Read input
n = int(input().strip())
a = list(map(int, input().strip().split()))

# Calculate and print the result
result = min_instability(n, a)
print(result)