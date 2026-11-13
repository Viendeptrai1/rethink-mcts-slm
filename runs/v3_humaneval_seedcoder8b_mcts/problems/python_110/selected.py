def exchange(lst1, lst2):
    if all(num % 2 == 0 for num in lst1):
        return "YES"
    
    odd_count = sum(1 for num in lst1 if num % 2 != 0)
    even_count = sum(1 for num in lst2 if num % 2 == 0)
    
    return "YES" if even_count >= odd_count else "NO"