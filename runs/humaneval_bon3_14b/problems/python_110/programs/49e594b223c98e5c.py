def exchange(lst1, lst2):
    # Check if there is at least one even number in lst2
    has_even_in_lst2 = any(x % 2 == 0 for x in lst2)
    
    # Check if all numbers in lst1 are already even
    all_even_in_lst1 = all(x % 2 == 0 for x in lst1)
    
    # If lst1 is already all even, or if lst2 has at least one even number, return "YES"
    if all_even_in_lst1 or has_even_in_lst2:
        return "YES"
    
    # Otherwise, it's not possible to make lst1 all even
    return "NO"