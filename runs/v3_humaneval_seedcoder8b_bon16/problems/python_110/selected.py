def exchange(lst1, lst2):
    even_count = sum(1 for num in lst1 if num % 2 == 0)
    if even_count == len(lst1):
        return "YES"
    
    odd_count = len(lst1) - even_count
    even_in_lst2 = sum(1 for num in lst2 if num % 2 == 0)
    
    if even_in_lst2 >= odd_count:
        return "YES"
    else:
        return "NO"