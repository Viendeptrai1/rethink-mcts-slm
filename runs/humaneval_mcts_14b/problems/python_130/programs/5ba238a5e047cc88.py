def tri(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # Initialize the sequence with base cases
    sequence = [0] * (n + 1)
    sequence[0] = 1  # Assuming tri(0) = 1 based on the pattern observed
    sequence[1] = 3
    
    for i in range(2, n + 1):
        if i % 2 == 0:
            sequence[i] = 1 + i // 2
        else:
            if i == 2:
                sequence[i] = sequence[i - 1] + sequence[i - 2] + sequence[i + 1]
            else:
                sequence[i] = sequence[i - 1] + sequence[i - 2] + sequence[i + 1]
    
    return sequence

# Example usage:
# print(tri(3))  # Output: [1, 3, 2, 8]