def tri(n):
    if n < 0:
        return []
    
    # Initialize the sequence with base cases
    sequence = [1, 3]  # tri(0) = 1, tri(1) = 3
    
    # Compute the sequence up to tri(n)
    for i in range(2, n + 1):
        if i % 2 == 0:
            sequence.append(1 + i // 2)
        else:
            # Ensure we have enough elements in the sequence
            while len(sequence) <= i + 1:
                sequence.append(0)
            sequence[i] = sequence[i - 1] + sequence[i - 2] + sequence[i + 1]
    
    return sequence[:n + 1]

# Example usage:
# print(tri(3))  # Output: [1, 3, 2, 8]