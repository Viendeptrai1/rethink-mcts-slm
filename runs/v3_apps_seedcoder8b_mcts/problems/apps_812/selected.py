def find_arithmetic_index(n, b):
    for j in range(n):
        # Create a new list without the j-th element
        remaining = b[:j] + b[j+1:]
        remaining.sort()
        
        # Check if the remaining list is an arithmetic progression
        if len(remaining) == 1:
            return j + 1
        
        c = remaining[1] - remaining[0]
        is_ap = True
        
        for i in range(2, len(remaining)):
            if remaining[i] - remaining[i-1] != c:
                is_ap = False
                break
        
        if is_ap:
            return j + 1
    
    return -1

# Read input
n = int(input())
b = list(map(int, input().split()))

# Find and print the result
result = find_arithmetic_index(n, b)
print(result)