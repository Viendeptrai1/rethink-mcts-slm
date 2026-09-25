def special_factorial(n):
    """The Brazilian factorial is defined as:
    brazilian_factorial(n) = n! * (n-1)! * (n-2)! * ... * 1!
    where n > 0

    For example:
    >>> special_factorial(4)
    288

    The function will receive an integer as input and should return the special
    factorial of this integer.
    """
    
    def factorial(num):
        if num == 0 or num == 1:
            return 1
        else:
            result = 1
            for i in range(2, num + 1):
                result *= i
            return result
    
    brazilian_factorial = 1
    for i in range(1, n + 1):
        brazilian_factorial *= factorial(i)
    
    return brazilian_factorial

# Example usage
print(special_factorial(4))  # Output: 288