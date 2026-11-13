def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    even_digits = {0, 2, 4, 6, 8}
    result = []
    
    start = min(a, b)
    end = max(a, b)
    
    for num in range(start, end + 1):
        for digit in str(num):
            if digit in even_digits:
                result.append(int(digit))
    
    return sorted(result)