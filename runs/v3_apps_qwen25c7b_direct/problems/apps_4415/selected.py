def split_sequence(a):
    n = len(a)
    if n == 1:
        return "YES\n1\n{}\n0".format(a[0])
    
    increasing = []
    decreasing = []
    i = 0
    
    while i < n - 1:
        if a[i] < a[i + 1]:
            increasing.append(a[i])
            while i < n - 1 and a[i] < a[i + 1]:
                increasing.append(a[i + 1])
                i += 1
        elif a[i] > a[i + 1]:
            decreasing.append(a[i])
            while i < n - 1 and a[i] > a[i + 1]:
                decreasing.append(a[i + 1])
                i += 1
        else:
            return "NO"
        i += 1
    
    if i == n - 1:
        if a[n - 1] > a[n - 2]:
            decreasing.append(a[n - 1])
        else:
            increasing.append(a[n - 1])
    
    if increasing and decreasing and increasing[-1] > decreasing[0]:
        return "NO"
    
    return "YES\n{} {}\n{} {}".format(len(increasing), ' '.join(map(str, increasing)), len(decreasing), ' '.join(map(str, decreasing)))

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

result = split_sequence(a)
print(result)