def min_operations_to_increasing(n, k, a, b):
    if k == 0:
        # If no elements are fixed, simply check if the array is already increasing
        operations = 0
        last_valid = float('-inf')
        for i in range(n):
            if a[i] <= last_valid:
                operations += 1
                a[i] = last_valid + 1
            last_valid = a[i]
        return operations

    # Create a set for quick lookup of fixed positions
    fixed_positions = set(b)

    # Initialize variables
    operations = 0
    last_valid = float('-inf')
    last_fixed_value = float('-inf')

    for i in range(n):
        if i + 1 in fixed_positions:
            # If the current position is fixed, ensure it's greater than the last fixed value
            if a[i] <= last_fixed_value:
                return -1  # Impossible to make the array increasing
            last_fixed_value = a[i]
        else:
            # If the current position is not fixed, ensure it's greater than the last valid value
            if a[i] <= last_valid:
                operations += 1
                a[i] = last_valid + 1
        last_valid = a[i]

    return operations

# Read input
n, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split())) if k > 0 else []

# Call the function and print the result
result = min_operations_to_increasing(n, k, a, b)
print(result)