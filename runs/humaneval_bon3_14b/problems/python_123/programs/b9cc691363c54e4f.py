def get_odd_collatz(n):
    """
    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.
    """
    if n <= 0:
        raise ValueError("Input must be a positive integer")
    
    odd_numbers = []
    
    while n != 1:
        if n % 2 == 1:
            odd_numbers.append(n)
        n = 3 * n + 1 if n % 2 == 1 else n // 2
    
    odd_numbers.append(1)  # Add the final 1 to the list
    return sorted(odd_numbers)

# Example usage:
# print(get_odd_collatz(5))  # Output: [1, 5]