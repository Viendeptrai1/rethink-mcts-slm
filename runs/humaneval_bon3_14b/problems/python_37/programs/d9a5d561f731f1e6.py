def sort_even(l: list):
    """This function takes a list l and returns a list l' such that
    l' is identical to l in the odd indicies, while its values at the even indicies are equal
    to the values of the even indicies of l, but sorted.
    """
    even_indices = [i for i in range(len(l)) if i % 2 == 0]
    even_values = [l[i] for i in even_indices]
    even_values.sort()
    
    l_prime = l[:]
    for idx, value in zip(even_indices, even_values):
        l_prime[idx] = value
    
    return l_prime

# Test cases
print(sort_even([1, 2, 3]))  # Output: [1, 2, 3]
print(sort_even([5, 6, 3, 4]))  # Output: [3, 6, 5, 4]