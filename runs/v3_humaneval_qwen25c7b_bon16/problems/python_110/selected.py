def exchange(lst1, lst2):
    odd_in_lst1 = [x for x in lst1 if x % 2 != 0]
    even_in_lst2 = [x for x in lst2 if x % 2 == 0]
    
    return "YES" if len(odd_in_lst1) <= len(even_in_lst2) else "NO"