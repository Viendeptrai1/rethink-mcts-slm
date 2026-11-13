def order_by_points(nums):
    def digit_sum(n):
        s = 0
        n = abs(n)
        while n > 0:
            s += n % 10
            n //= 10
        return s

    indexed_nums = list(enumerate(nums))
    indexed_nums.sort(key=lambda x: (digit_sum(x[1]), x[0]))
    return [num for _, num in indexed_nums]