import sys

def min_partition_sum(a, c):
    n = len(a)
    if n == 1:
        return a[0]
    
    # Sort the array in descending order
    a.sort(reverse=True)
    
    total_sum = 0
    for i in range(0, n, c):
        # Sum up the elements except for the floor(k/c) smallest ones
        k = min(c, n - i)
        total_sum += sum(a[i:i+k]) - sum(sorted(a[i:i+k])[:k//c])
    
    return total_sum

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
c = int(data[1])
a = list(map(int, data[2:]))

# Calculate and print the result
print(min_partition_sum(a, c))