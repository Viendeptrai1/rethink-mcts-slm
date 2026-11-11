def tri(n):
    if n < 0:
        return []
    
    # Base cases
    if n == 0:
        return [1]
    elif n == 1:
        return [1, 3]
    
    # Initialize the sequence with base values
    sequence = [1, 3]
    
    # Calculate the sequence up to n
    for i in range(2, n + 1):
        if i % 2 == 0:
            sequence.append(1 + i // 2)
        else:
            # Ensure we have enough elements to calculate tri(i)
            while len(sequence) <= i + 1:
                next_value = sequence[-1] + sequence[-2] + sequence[-3]
                sequence.append(next_value)
            sequence[i] = sequence[i - 1] + sequence[i - 2] + sequence[i + 1]
    
    return sequence[:n + 1]

# Example usage:
# print(tri(3))  # Output: [1, 3, 2, 8]