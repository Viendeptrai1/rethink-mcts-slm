def min_problems_to_add(n, m, a, b):
    # Sort the required complexities and the prepared complexities
    a.sort()
    b.sort()
    
    # Initialize pointers for both lists
    i, j = 0, 0
    # Initialize the count of problems to add
    problems_to_add = 0
    
    # Iterate over the required complexities
    while i < n:
        # If the current prepared problem can be simplified to match the required complexity
        if j < m and b[j] >= a[i]:
            j += 1
        else:
            # Otherwise, we need to add a new problem
            problems_to_add += 1
        i += 1
    
    return problems_to_add

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