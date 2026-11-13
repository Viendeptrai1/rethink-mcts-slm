def unique_digits(x):
    def has_even_digit(num):
        return any(int(digit) % 2 == 0 for digit in str(num))

    return sorted([num for num in x if not has_even_digit(num)])