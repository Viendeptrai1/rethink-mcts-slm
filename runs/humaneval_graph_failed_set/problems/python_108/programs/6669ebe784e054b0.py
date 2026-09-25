def count_nums(arr):
    def digit_sum(n):
        # Convert number to string to iterate over each character
        str_n = str(n)
        # Initialize sum
        total = 0
        # Handle the first character if it's a negative sign
        if str_n[0] == '-':
            total += int(str_n[0] + str_n[1])
            start_index = 2
        else:
            start_index = 0
        # Add remaining digits
        for char in str_n[start_index:]:
            total += int(char)
        return total

    count = 0
    for num in arr:
        if digit_sum(num) > 0:
            count += 1
    return count

# Test cases
print(count_nums([]))          # Output: 0
print(count_nums([-1, 11, -11])) # Output: 1
print(count_nums([1, 1, 2]))   # Output: 3