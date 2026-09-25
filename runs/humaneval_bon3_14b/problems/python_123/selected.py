def get_odd_collatz(n):
    """
    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.
    """
    if n <= 0:
        raise ValueError("Input must be a positive integer")
    
    collatz_sequence = []
    while n != 1:
        if n % 2 == 1:
            collatz_sequence.append(n)
        n = 3 * n + 1 if n % 2 == 1 else n // 2
    
    # Add the final 1 to the sequence
    collatz_sequence.append(1)
    
    # Return the sorted list of odd numbers
    return sorted(collatz_sequence)

# Example usage:
# print(get_odd_collatz(5))  # Output: [1, 5]