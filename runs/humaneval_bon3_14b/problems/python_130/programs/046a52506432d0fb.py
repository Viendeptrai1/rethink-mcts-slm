def tri(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # Initialize the sequence with base cases
    sequence = [0] * (n + 1)
    sequence[0] = 1  # tri(0) is not defined in the problem, but we start from 0 for indexing
    sequence[1] = 3
    
    for i in range(2, n + 1):
        if i % 2 == 0:
            sequence[i] = 1 + i // 2
        else:
            if i == 1:
                continue
            sequence[i] = sequence[i - 1] + sequence[i - 2] + (sequence[i + 1] if i + 1 <= n else 3)
    
    return sequence[:n + 1]

# Example usage:
# print(tri(3))  # Output: [1, 3, 2, 8]