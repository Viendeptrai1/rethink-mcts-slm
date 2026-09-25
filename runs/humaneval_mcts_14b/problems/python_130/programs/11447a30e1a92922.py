def tri(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # Initialize the sequence with known values
    sequence = [0] * (n + 1)
    sequence[0] = 1  # Define tri(0) = 1 based on the problem statement
    
    for i in range(1, n + 1):
        if i == 1:
            sequence[i] = 3
        elif i % 2 == 0:
            sequence[i] = 1 + i // 2
        else:
            sequence[i] = sequence[i - 1] + sequence[i - 2] + sequence[i + 1] if i + 1 <= n else sequence[i - 1] + sequence[i - 2]
    
    return sequence

# Example usage:
# print(tri(3))  # Output: [1, 3, 2, 8]