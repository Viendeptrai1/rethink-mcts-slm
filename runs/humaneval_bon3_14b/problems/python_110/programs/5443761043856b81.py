def exchange(lst1, lst2):
    # Check if there is at least one even number in lst2
    has_even_in_lst2 = any(x % 2 == 0 for x in lst2)
    
    # Check if all numbers in lst1 are already even
    all_even_in_lst1 = all(x % 2 == 0 for x in lst1)
    
    # If all numbers in lst1 are already even, return "YES"
    if all_even_in_lst1:
        return "YES"
    
    # If there is at least one even number in lst2 and not all numbers in lst1 are even, return "YES"
    if has_even_in_lst2:
        return "YES"
    
    # Otherwise, return "NO"
    return "NO"