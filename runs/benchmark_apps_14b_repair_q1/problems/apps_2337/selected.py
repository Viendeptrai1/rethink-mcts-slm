def min_problems_to_add(n, m, a, b):
    # Sort the required complexities and the prepared complexities
    a.sort()
    b.sort()
    
    # Initialize pointers for both lists
    i, j = 0, 0
    additional_problems = 0
    
    # Iterate over the required complexities
    while i < n:
        # Find the first prepared problem that can be simplified to match the required complexity
        while j < m and b[j] < a[i]:
            j += 1
        
        # If we have found a suitable problem or run out of prepared problems
        if j < m:
            j += 1
        else:
            # Otherwise, we need to add a new problem
            additional_problems += 1
        
        i += 1
    
    return additional_problems

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2+n]))
b = list(map(int, data[2+n:2+n+m]))

# Output the result
print(min_problems_to_add(n, m, a, b))