def unique_digits(x):
    """Given a list of positive integers x, return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
    def has_no_even_digit(n):
        for digit in str(n):
            if int(digit) % 2 == 0:
                return False
        return True

    result = [num for num in x if has_no_even_digit(num)]
    return sorted(result)

# Example usage
if __name__ == "__main__":
    print(unique_digits([15, 33, 1422, 1]))  # Output: [1, 15, 33]
    print(unique_digits([152, 323, 1422, 10]))  # Output: []