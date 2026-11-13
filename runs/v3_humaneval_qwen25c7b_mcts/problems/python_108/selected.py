def count_nums(arr):
    def sum_of_digits(n):
        if n >= 0:
            return sum(int(digit) for digit in str(n))
        else:
            digits = [int(d) for d in str(n)[1:]]
            digits[0] *= -1
            return sum(digits)
    
    return sum(1 for num in arr if sum_of_digits(num) > 0)