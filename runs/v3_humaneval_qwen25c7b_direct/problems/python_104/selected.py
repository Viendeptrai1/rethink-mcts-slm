def unique_digits(x):
    def has_no_even_digit(num):
        while num > 0:
            if (num % 10) % 2 == 0:
                return False
            num //= 10
        return True

    return sorted(filter(has_no_even_digit, x))