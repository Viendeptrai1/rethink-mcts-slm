def sort_array(arr):
    """
    Sorts an array of non-negative integers according to the number of ones in their binary
    representation in ascending order. For numbers with the same number of ones, sort them by their
    decimal values.
    """
    return sorted(arr, key=lambda x: (bin(x).count('1'), x))