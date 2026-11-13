def total_match(lst1, lst2):
    def count_chars(lst):
        return sum(len(s) for s in lst)
    
    count1 = count_chars(lst1)
    count2 = count_chars(lst2)
    
    if count1 <= count2:
        return lst1
    else:
        return lst2