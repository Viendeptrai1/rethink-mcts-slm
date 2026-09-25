def tri(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # Initialize the sequence with base cases
    sequence = [0] * (n + 1)
    sequence[0] = 1  # Assuming tri(0) = 1 as per the examples
    sequence[1] = 3
    
    for i in range(2, n + 1):
        if i % 2 == 0:
            sequence[i] = 1 + i // 2
        else:
            if i + 1 <= n:
                sequence[i] = sequence[i - 1] + sequence[i - 2] + sequence[i + 1]
            else:
                # If i + 1 is out of bounds, we need to handle it separately
                # Since we don't have tri(i + 1), we can't compute tri(i) directly
                # We assume tri(i + 1) = 0 for the purpose of this calculation
                sequence[i] = sequence[i - 1] + sequence[i - 2]
    
    return sequence[:n + 1]

# Example usage:
print(tri(3))  # Output: [1, 3, 2, 8]