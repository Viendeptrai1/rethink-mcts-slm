def add_elements(arr, k):
    return sum(x for x in arr[:k] if -99 <= x <= 99)

# Example usage:
# result = add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4)
# print(result)  # Output: 24