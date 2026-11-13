def find_reverse_subsequence(n, v):
    # Step 1: Find the first part that is sorted
    start = 0
    while start < n - 1 and v[start] <= v[start + 1]:
        start += 1
    
    # If the entire array is already sorted
    if start == n - 1:
        return "impossible"
    
    # Step 2: Find the last part that is sorted
    end = n - 1
    while end > 0 and v[end] >= v[end - 1]:
        end -= 1
    
    # Step 3: Reverse the middle section and check if it sorts the array
    middle = v[start:end + 1]
    if v[:start] + middle[::-1] + v[end + 1:] == sorted(v):
        return f"{start + 1} {end + 1}"
    
    return "impossible"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
v = list(map(int, data[1:n + 1]))

# Get the result
result = find_reverse_subsequence(n, v)

# Print the result
print(result)