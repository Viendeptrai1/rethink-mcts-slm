def can_split_sequence(n, a):
    if n == 1:
        return "YES", [0]
    
    increasing = []
    decreasing = []
    
    res = []
    
    for i in range(n):
        if not increasing or a[i] > increasing[-1]:
            increasing.append(a[i])
            res.append(0)
        elif not decreasing or a[i] < decreasing[-1]:
            decreasing.append(a[i])
            res.append(1)
        else:
            return "NO", []
    
    return "YES", res

# Read input
n = int(input())
a = list(map(int, input().split()))

# Get the result
result, res_sequence = can_split_sequence(n, a)

# Print the result
print(result)
if result == "YES":
    print(" ".join(map(str, res_sequence)))