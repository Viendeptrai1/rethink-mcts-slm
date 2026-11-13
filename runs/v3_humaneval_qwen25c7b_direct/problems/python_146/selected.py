def specialFilter(nums):
    def is_odd_and_greater_than_10(num):
        if num <= 10:
            return False
        str_num = str(abs(num))
        return int(str_num[0]) % 2 == 1 and int(str_num[-1]) % 2 == 1
    
    return sum(is_odd_and_greater_than_10(num) for num in nums)