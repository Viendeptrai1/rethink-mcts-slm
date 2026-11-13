def total_match(lst1, lst2):
    def count_chars(lst):
        return sum(len(s) for s in lst)
    
    chars1 = count_chars(lst1)
    chars2 = count_chars(lst2)
    
    if chars1 <= chars2:
        return lst1
    else:
        return lst2