def split_sequence(a):
    n = len(a)
    if n == 1:
        return "YES", [0]
    
    increasing = []
    decreasing = []
    i = 0
    
    while i < n - 1 and a[i] < a[i + 1]:
        increasing.append(a[i])
        i += 1
    
    if i == n - 1:
        return "NO", []
    
    decreasing.append(a[i])
    i += 1
    
    while i < n and a[i] < a[i - 1]:
        decreasing.append(a[i])
        i += 1
    
    if i != n:
        return "NO", []
    
    result = [1 if x in decreasing else 0 for x in a]
    return "YES", result

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

result, res = split_sequence(a)
print(result)
if result == "YES":
    print(" ".join(map(str, res)))