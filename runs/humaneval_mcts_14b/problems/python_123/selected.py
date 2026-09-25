def get_odd_collatz(n):
    """
    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.
    """
    odd_numbers = []
    
    while n != 1:
        if n % 2 == 1:
            odd_numbers.append(n)
        n = 3 * n + 1 if n % 2 == 1 else n // 2
    
    odd_numbers.append(1)  # Add 1 to the list as it is part of the sequence and is odd.
    
    return sorted(odd_numbers)

# Example usage:
# print(get_odd_collatz(5))  # Output: [1, 5]