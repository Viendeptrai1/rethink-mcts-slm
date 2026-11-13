def minimum_additional_problems(n, m, a, b):
    # Sort the list of prepared problem complexities
    b.sort()
    
    # Initialize pointers and counters
    j = 0  # Pointer for the required complexities
    additional_problems = 0  # Counter for additional problems needed
    
    # Iterate over the prepared problems
    for i in range(m):
        # If the current prepared problem meets the current required complexity
        if j < n and b[i] >= a[j]:
            j += 1  # Move to the next required complexity
        else:
            # If it doesn't meet, we need to add a new problem
            additional_problems += 1
    
    # If there are still required complexities that haven't been met
    additional_problems += n - j
    
    return additional_problems

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:]))

# Output the result
print(minimum_additional_problems(n, m, a, b))