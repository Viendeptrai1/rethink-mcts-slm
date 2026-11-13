def double_the_difference(lst):
    def is_valid_odd(num):
        return isinstance(num, int) and num > 0 and num % 2 != 0

    return sum(num ** 2 for num in filter(is_valid_odd, lst))