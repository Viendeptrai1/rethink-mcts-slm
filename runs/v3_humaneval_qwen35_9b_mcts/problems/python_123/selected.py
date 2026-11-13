def get_odd_collatz(n):
    """
    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.
    """
    odd_numbers = []
    current = n
    
    while current != 1:
        if current % 2 != 0:
            odd_numbers.append(current)
            current = 3 * current + 1
        else:
            current = current // 2
    
    odd_numbers.append(1)
    odd_numbers.sort()
    
    return odd_numbers