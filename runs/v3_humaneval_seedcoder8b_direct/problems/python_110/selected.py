def exchange(lst1, lst2):
    even_count = sum(1 for num in lst1 if num % 2 == 0)
    if even_count == len(lst1):
        return "YES"
    
    odd_in_lst1 = [num for num in lst1 if num % 2 != 0]
    even_in_lst2 = [num for num in lst2 if num % 2 == 0]
    
    if not odd_in_lst1 or not even_in_lst2:
        return "NO"
    
    return "YES"