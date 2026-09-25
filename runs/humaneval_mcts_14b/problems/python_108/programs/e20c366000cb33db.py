def count_nums(arr):
    def sum_of_digits(num):
        num_str = str(num)
        if num_str[0] == '-':
            return int(num_str[0] + num_str[1]) + sum(int(digit) for digit in num_str[2:])
        else:
            return sum(int(digit) for digit in num_str)
    
    count = 0
    for num in arr:
        if sum_of_digits(num) > 0:
            count += 1
    return count

# Test cases
print(count_nums([]))          # Output: 0
print(count_nums([-1, 11, -11]))  # Output: 1
print(count_nums([1, 1, 2]))     # Output: 3