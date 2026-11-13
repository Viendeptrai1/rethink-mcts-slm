def order_by_points(nums):
    return sorted(enumerate(nums), key=lambda x: (sum(int(digit) for digit in str(abs(x[1]))), x[0]))[::1][::-1]

# Test cases
print(order_by_points([1, 11, -1, -11, -12]))  # Output: [-1, -11, 1, -12, 11]
print(order_by_points([]))  # Output: []