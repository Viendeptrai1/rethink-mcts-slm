import sys

def find_minimum_i(n, k, A):
    # Check if any element in A^0 is already >= k
    if any(x >= k for x in A):
        return 0
    
    # Initialize the running total with A^0
    running_total = A[:]
    
    # Iterate to compute A^i
    i = 0
    while True:
        i += 1
        # Update the running total for the next iteration
        for j in range(1, n):
            running_total[j] += running_total[j - 1]
        
        # Check if any element in the current running total is >= k
        if any(x >= k for x in running_total):
            return i

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
A = list(map(int, data[2:]))

# Find and print the minimum i
print(find_minimum_i(n, k, A))