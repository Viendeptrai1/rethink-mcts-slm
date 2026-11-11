def unique_digits(x):
    def has_only_odd_digits(num):
        return all(int(digit) % 2 != 0 for digit in str(num))
    
    result = [num for num in x if has_only_odd_digits(num)]
    return sorted(result)

# Example usage:
# print(unique_digits([15, 33, 1422, 1]))  # Output: [1, 15, 33]
# print(unique_digits([152, 323, 1422, 10]))  # Output: []