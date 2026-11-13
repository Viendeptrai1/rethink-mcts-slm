def split_sequence(n, a):
    increasing = [0] * n
    decreasing = [0] * n
    
    # Check for increasing subsequence
    i = 0
    while i + 1 < n and a[i] < a[i + 1]:
        increasing[i] = 1
        i += 1
    
    # Check for decreasing subsequence starting from the next element
    j = i + 1
    while j + 1 < n and a[j] > a[j + 1]:
        decreasing[j] = 1
        j += 1
    
    # If we have found both increasing and decreasing subsequences
    if i == n - 1 and j == n - 1:
        return "YES", increasing + decreasing[len(increasing):]
    
    # Check if the entire sequence is increasing or decreasing
    if i == n - 1:
        return "YES", [1] * n
    if j == n - 1:
        return "YES", [0] * n
    
    return "NO", []

# Input reading
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Output
result, seq = split_sequence(n, a)
print(result)
if result == "YES":
    print(" ".join(map(str, seq)))