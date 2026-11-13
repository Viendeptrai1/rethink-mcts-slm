def count_nums(arr):
    def sum_of_signed_digits(n):
        if n == 0:
            return 0
        is_negative = n < 0
        n = abs(n)
        total = 0
        while n > 0:
            digit = n % 10
            if is_negative and digit == 0:
                # This logic is flawed because we need to know if it's the first digit
                pass
            total += digit
            n //= 10
        if is_negative:
            # The first digit (most significant) should be negative
            # We need to recalculate to handle the sign correctly
            pass
        return total

    # Let's rewrite the helper function properly
    def get_signed_digit_sum(n):
        if n == 0:
            return 0
        s = str(n)
        if s[0] == '-':
            # Negative number: first digit is negative, rest are positive
            first_digit = int(s[1])
            rest_sum = sum(int(d) for d in s[2:])
            return -first_digit + rest_sum
        else:
            # Positive number: all digits are positive
            return sum(int(d) for d in s)

    count = 0
    for num in arr:
        if get_signed_digit_sum(num) > 0:
            count += 1
    return count