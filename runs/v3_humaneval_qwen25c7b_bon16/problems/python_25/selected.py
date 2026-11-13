from typing import List

def factorize(n: int) -> List[int]:
    factors = []
    # Start with the smallest prime number
    divisor = 2
    while n >= divisor * divisor:
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1
    if n > 1:
        factors.append(n)
    return factors