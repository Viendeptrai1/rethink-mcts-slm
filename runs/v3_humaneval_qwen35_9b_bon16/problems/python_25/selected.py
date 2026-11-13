from typing import List


def factorize(n: int) -> List[int]:
    """ Return list of prime factors of given integer in the order from smallest to largest.
    Each of the factors should be listed number of times corresponding to how many times it appeares in factorization.
    Input number should be equal to the product of all factors
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(25)
    [5, 5]
    >>> factorize(70)
    [2, 5, 7]
    """
    if n <= 1:
        return []

    factors: List[int] = []
    d = 2
    temp = n

    # Check for factor 2 separately to allow skipping even numbers later
    while temp % d == 0:
        factors.append(d)
        temp //= d

    d = 3
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 2

    # If temp is a prime number greater than 2
    if temp > 1:
        factors.append(temp)

    return factors