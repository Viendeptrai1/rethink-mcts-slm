def specialFilter(nums):
    def is_odd_digit(digit):
        return digit in {'1', '3', '5', '7', '9'}
    
    count = 0
    for num in nums:
        if num > 10:
            num_str = str(num)
            if is_odd_digit(num_str[0]) and is_odd_digit(num_str[-1]):
                count += 1
    return count