from functools import cmp_to_key

def order_by_points(nums):
    def sum_digits(n):
        s = str(n)
        total = 0
        for char in s:
            if char != '-':
                total += int(char)
        return total

    def compare(a, b):
        sum_a = sum_digits(a)
        sum_b = sum_digits(b)
        if sum_a != sum_b:
            return sum_a - sum_b
        return a.__index__ - b.__index__ if hasattr(a, '__index__') else (a - b) if isinstance(a, int) and isinstance(b, int) else 0

    # Since lists don't have index attributes that can be directly compared in a stable sort way with custom key,
    # we use a stable sort with a key that includes the original index.
    indexed_nums = list(enumerate(nums))
    sorted_indexed = sorted(indexed_nums, key=lambda x: (sum_digits(x[1]), x[0]))
    return [num for idx, num in sorted_indexed]

def order_by_points(nums):
    """
    Write a function which sorts the given list of integers
    in ascending order according to the sum of their digits.
    Note: if there are several items with similar sum of their digits,
    order them based on their index in original list.
    """
    def sum_digits(n):
        s = str(abs(n))
        return sum(int(d) for d in s)

    indexed_nums = list(enumerate(nums))
    sorted_indexed = sorted(indexed_nums, key=lambda x: (sum_digits(x[1]), x[0]))
    return [num for idx, num in sorted_indexed]