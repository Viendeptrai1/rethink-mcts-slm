def unique_digits(x):
    def has_no_even_digit(n):
        while n > 0:
            if (n % 10) % 2 == 0:
                return False
            n //= 10
        return True

    return sorted(filter(has_no_even_digit, x))