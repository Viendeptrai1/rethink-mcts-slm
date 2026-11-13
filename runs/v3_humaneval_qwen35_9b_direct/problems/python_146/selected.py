def specialFilter(nums):
    def is_first_and_last_digit_odd(n):
        # Work with absolute value to handle negative numbers correctly for digit extraction
        n = abs(n)
        
        # Check if the number is 0 (though 0 doesn't have odd first/last digits)
        if n == 0:
            return False
        
        first_digit = n
        while first_digit >= 10:
            first_digit //= 10
        
        last_digit = n % 10
        
        # Check if both first and last digits are odd
        return (first_digit % 2 == 1) and (last_digit % 2 == 1)

    count = 0
    for num in nums:
        # Condition 1: greater than 10
        if num > 10:
            # Condition 2: first and last digits are odd
            if is_first_and_last_digit_odd(num):
                count += 1
                
    return count