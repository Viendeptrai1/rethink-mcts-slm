def specialFilter(nums):
    def is_odd(n):
        return n % 2 != 0

    count = 0
    for num in nums:
        if num > 10:
            str_num = str(abs(num))
            if is_odd(int(str_num[0])) and is_odd(int(str_num[-1])):
                count += 1
    return count