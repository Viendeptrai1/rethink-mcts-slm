def specialFilter(nums):
    def is_odd_digit(num):
        return str(abs(num))[0] in '13579' and str(abs(num))[-1] in '13579'

    return sum(1 for num in nums if num > 10 and is_odd_digit(num))