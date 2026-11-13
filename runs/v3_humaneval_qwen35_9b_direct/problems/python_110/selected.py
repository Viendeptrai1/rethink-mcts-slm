def exchange(lst1, lst2):
    """In this problem, you will implement a function that takes two lists of numbers,
    and determines whether it is possible to perform an exchange of elements
    between them to make lst1 a list of only even numbers.
    There is no limit on the number of exchanged elements between lst1 and lst2.
    If it is possible to exchange elements between the lst1 and lst2 to make
    all the elements of lst1 to be even, return "YES".
    Otherwise, return "NO".
    For example:
    exchange([1, 2, 3, 4], [1, 2, 3, 4]) => "YES"
    exchange([1, 2, 3, 4], [1, 5, 3, 4]) => "NO"
    It is assumed that the input lists will be non-empty.
    """
    # Check if lst1 already contains only even numbers
    if all(num % 2 == 0 for num in lst1):
        return "YES"
    
    # Check if there is at least one even number in lst2
    # If there is, we can swap an odd number from lst1 with an even number from lst2
    # to reduce the count of odd numbers in lst1. We can repeat this until all odd numbers are gone.
    # Therefore, if lst1 has any odd numbers and lst2 has at least one even number, it's possible.
    has_even_in_lst2 = any(num % 2 == 0 for num in lst2)
    
    if has_even_in_lst2:
        return "YES"
    else:
        return "NO"