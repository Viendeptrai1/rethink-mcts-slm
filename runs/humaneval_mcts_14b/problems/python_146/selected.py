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

# Example usage:
# print(specialFilter([15, -73, 14, -15]))  # Output: 1
# print(specialFilter([33, -2, -3, 45, 21, 109]))  # Output: 2