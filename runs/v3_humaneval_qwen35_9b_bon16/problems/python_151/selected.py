def double_the_difference(lst):
    total = 0
    for num in lst:
        # Check if the number is an integer
        if not isinstance(num, int):
            continue
        # Ignore negative numbers
        if num < 0:
            continue
        # Check if the number is odd
        if num % 2 != 0:
            total += num * num
    return total