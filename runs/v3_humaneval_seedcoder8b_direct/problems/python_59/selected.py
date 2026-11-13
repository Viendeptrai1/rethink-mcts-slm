def largest_prime_factor(n: int):
    largest = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            largest = i
            n //= i
        else:
            i += 1
    if n > 1:
        largest = n
    return largest