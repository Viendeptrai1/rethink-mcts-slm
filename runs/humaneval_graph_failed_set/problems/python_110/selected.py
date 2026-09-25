def exchange(lst1, lst2):
    # Helper function to count odd numbers in a list
    def count_odds(lst):
        return sum(1 for x in lst if x % 2 != 0)
    
    # Helper function to count even numbers in a list
    def count_evens(lst):
        return sum(1 for x in lst if x % 2 == 0)
    
    # Count the number of odd numbers in lst1
    odd_count_lst1 = count_odds(lst1)
    
    # Count the number of even numbers in lst2
    even_count_lst2 = count_evens(lst2)
    
    # Check if we have enough even numbers in lst2 to replace all odd numbers in lst1
    if even_count_lst2 >= odd_count_lst1:
        return "YES"
    else:
        return "NO"