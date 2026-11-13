def count_nums(arr):
    def sum_of_digits(num):
        if num < 0:
            return int(str(num)[0]) + sum(int(digit) for digit in str(num)[1:])
        else:
            return sum(int(digit) for digit in str(num))
    
    return sum(1 for num in arr if sum_of_digits(num) > 0)