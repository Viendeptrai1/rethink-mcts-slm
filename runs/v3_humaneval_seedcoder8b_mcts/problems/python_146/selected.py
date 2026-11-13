def specialFilter(nums):
    def is_odd_digit(num):
        return int(str(abs(num))[0]) % 2 == 1 and int(str(abs(num))[-1]) % 2 == 1

    return sum(1 for num in nums if num > 10 and is_odd_digit(num))