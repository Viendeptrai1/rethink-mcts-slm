def sort_even(l: list):
    """This function takes a list l and returns a list l' such that
    l' is identical to l in the odd indicies, while its values at the even indicies are equal
    to the values of the even indicies of l, but sorted.
    >>> sort_even([1, 2, 3])
    [1, 2, 3]
    >>> sort_even([5, 6, 3, 4])
    [3, 6, 5, 4]
    """
    # Extract values at even indices
    even_indices = [i for i in range(0, len(l), 2)]
    even_values = [l[i] for i in even_indices]
    
    # Sort the even-indexed values
    even_values.sort()
    
    # Reconstruct the list
    result = l.copy()
    for idx, val in zip(even_indices, even_values):
        result[idx] = val
    
    return result