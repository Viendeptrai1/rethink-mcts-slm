def order_by_points(nums):
    def sum_of_digits(n):
        s = 0
        n = abs(n)
        while n > 0:
            s += n % 10
            n //= 10
        return s

    indexed_nums = list(enumerate(nums))
    indexed_nums.sort(key=lambda x: (sum_of_digits(x[1]), x[0]))
    return [num for idx, num in indexed_nums]