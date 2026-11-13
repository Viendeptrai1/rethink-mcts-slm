def unique_digits(x):
    def has_only_odd_digits(n):
        while n > 0:
            digit = n % 10
            if digit % 2 == 0:
                return False
            n //= 10
        return True

    result = [num for num in x if has_only_odd_digits(num)]
    return sorted(result)