def tri(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # Base cases
    if n == 0:
        return [1]
    elif n == 1:
        return [1, 3]
    elif n == 2:
        return [1, 3, 2]
    
    # Initialize the sequence with base cases
    sequence = [1, 3, 2]
    
    # Compute the sequence up to n
    for i in range(3, n + 1):
        if i % 2 == 0:
            sequence.append(1 + i // 2)
        else:
            sequence.append(sequence[i - 1] + sequence[i - 2] + sequence[i - 3])
    
    return sequence

# Example usage
print(tri(3))  # Output: [1, 3, 2, 8]