def is_prime(n):
    """Helper function to check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def x_or_y(n, x, y):
    """Returns x if n is a prime number, otherwise returns y."""
    if is_prime(n):
        return x
    else:
        return y

# Example usage:
# print(x_or_y(7, 34, 12))  # Output: 34
# print(x_or_y(15, 8, 5))   # Output: 5