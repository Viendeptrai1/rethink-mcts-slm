def min_operations_to_increasing(n, k, a, b):
    if k == 0:
        # If no elements in set b, we can freely change any element
        operations = 0
        last = 0
        for i in range(n):
            if a[i] <= last:
                operations += 1
                last += 1
            else:
                last = a[i]
        return operations

    # Convert b to a set for O(1) lookups
    b_set = set(b)
    
    # Create a new list to store the modified array
    modified_a = a[:]
    
    # First pass: make the array increasing by modifying non-b elements
    last = 0
    for i in range(n):
        if i + 1 in b_set:
            if modified_a[i] <= last:
                return -1  # Impossible to make increasing
            last = modified_a[i]
        else:
            if modified_a[i] <= last:
                modified_a[i] = last + 1
            last = modified_a[i]
    
    # Second pass: count operations needed to make the array increasing
    operations = 0
    last = 0
    for i in range(n):
        if modified_a[i] <= last:
            operations += 1
            last += 1
        else:
            last = modified_a[i]
    
    return operations

# Read input
n, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split())) if k > 0 else []

# Calculate and print result
result = min_operations_to_increasing(n, k, a, b)
print(result)