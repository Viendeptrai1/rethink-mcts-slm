def tri(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # Initialize the sequence with known values
    sequence = [1, 3]
    
    # Compute the sequence up to tri(n)
    for i in range(2, n + 1):
        if i % 2 == 0:
            sequence.append(1 + i // 2)
        else:
            # Precompute tri(n + 1) if needed
            if i == n:
                sequence.append(1 + (i + 1) // 2)
            else:
                sequence.append(sequence[i - 1] + sequence[i - 2] + sequence[i + 1])
    
    return sequence[:n + 1]

# Example usage
print(tri(3))  # Output: [1, 3, 2, 8]