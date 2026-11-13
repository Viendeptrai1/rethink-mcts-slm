def count_nums(arr):
    """
    Write a function count_nums which takes an array of integers and returns
    the number of elements which has a sum of digits > 0.
    If a number is negative, then its first signed digit will be negative:
    e.g. -123 has signed digits -1, 2, and 3.
    """
    def sum_signed_digits(n):
        s = 0
        if n < 0:
            # Handle negative numbers by processing sign first
            sign = -1
            n = abs(n)
            while n > 0:
                digit = n % 10
                if n // 10 == 0:
                    # First digit (most significant) gets the negative sign
                    s += sign * digit
                else:
                    s += digit
                n //= 10
        else:
            while n > 0:
                digit = n % 10
                s += digit
                n //= 10
        return s

    count = 0
    for num in arr:
        if sum_signed_digits(num) > 0:
            count += 1
    return count