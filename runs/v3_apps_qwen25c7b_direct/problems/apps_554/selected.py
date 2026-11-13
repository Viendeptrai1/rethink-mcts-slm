def max_happiness(n, m, a, subarrays):
    # Initialize a list to keep track of the contribution of each flower
    contributions = [0] * n
    
    # Iterate over each subarray
    for l, r in subarrays:
        # Increment the contribution for each flower in the current subarray
        for i in range(l - 1, r):
            contributions[i] += a[i]
    
    # Return the sum of the absolute values of the contributions
    return sum(abs(x) for x in contributions)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2+n]))
subarrays = []

for i in range(m):
    l = int(data[2+n+2*i]) - 1
    r = int(data[2+n+2*i+1]) - 1
    subarrays.append((l, r))

# Calculate and print the result
print(max_happiness(n, m, a, subarrays))