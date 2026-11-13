def specialFilter(nums):
    def is_first_and_last_digit_odd(n):
        n = abs(n)
        if n < 10:
            return False
        first_digit = n // 10 ** (len(str(n)) - 1)
        last_digit = n % 10
        return first_digit % 2 == 1 and last_digit % 2 == 1

    count = 0
    for num in nums:
        if num > 10 and is_first_and_last_digit_odd(num):
            count += 1
    return count