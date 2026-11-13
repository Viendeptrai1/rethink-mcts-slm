def exchange(lst1, lst2):
    odd_count_lst1 = sum(1 for x in lst1 if x % 2 != 0)
    even_count_lst2 = sum(1 for x in lst2 if x % 2 == 0)
    
    return "YES" if even_count_lst2 >= odd_count_lst1 else "NO"