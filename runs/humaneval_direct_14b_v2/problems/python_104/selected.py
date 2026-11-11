def unique_digits(x):
    def has_no_even_digit(num):
        while num > 0:
            digit = num % 10
            if digit % 2 == 0:
                return False
            num //= 10
        return True

    result = [num for num in x if has_no_even_digit(num)]
    result.sort()
    return result