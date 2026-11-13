def find_sequences(n, a):
    max_len = 0
    start = 0
    end = 0
    
    for i in range(1, n):
        if a[i] <= a[i - 1]:
            break
        end = i
    
    if end == n - 1:
        return "NO"
    
    for i in range(end, n - 1):
        if a[i] >= a[i + 1]:
            break
        end = i + 1
    
    if end != n - 1:
        return "NO"
    
    increasing = a[:end + 1]
    decreasing = a[end:]
    
    return "YES\n{}\n{}\n{}\n{}".format(len(increasing), ' '.join(map(str, increasing)), len(decreasing), ' '.join(map(str, decreasing[::-1])))

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output result
result = find_sequences(n, a)
print(result)