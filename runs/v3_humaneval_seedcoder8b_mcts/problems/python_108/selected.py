def count_nums(arr):
    def digit_sum(num):
        if num == 0:
            return 0
        digits = [int(d) for d in str(abs(num))]
        if num < 0:
            digits[0] = -digits[0]
        return sum(digits)

    return sum(1 for num in arr if digit_sum(num) > 0)