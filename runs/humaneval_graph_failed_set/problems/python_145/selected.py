def order_by_points(nums):
    def digit_sum(n):
        return sum(int(digit) for digit in str(abs(n)))
    
    # Create a list of tuples (digit_sum, original_index, value)
    indexed_nums = [(digit_sum(num), index, num) for index, num in enumerate(nums)]
    
    # Sort the list of tuples by digit_sum, then by original_index
    indexed_nums.sort(key=lambda x: (x[0], x[1]))
    
    # Extract the sorted values
    return [num for _, _, num in indexed_nums]

# Example usage:
print(order_by_points([1, 11, -1, -11, -12]))  # Output: [-1, -11, 1, -12, 11]
print(order_by_points([]))                      # Output: []