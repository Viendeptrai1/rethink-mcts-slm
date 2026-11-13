def count_nums(arr):
    def sum_of_signed_digits(n):
        if n == 0:
            return 0
        sign = -1 if n < 0 else 1
        n = abs(n)
        total = 0
        while n > 0:
            digit = n % 10
            if n < 0:
                total -= digit
            else:
                total += digit
            n //= 10
        return total

    count = 0
    for num in arr:
        if sum_of_signed_digits(num) > 0:
            count += 1
    return count