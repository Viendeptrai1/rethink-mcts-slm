def exchange(lst1, lst2):
    # Count the number of odd numbers in lst1
    odd_count_lst1 = sum(1 for x in lst1 if x % 2 != 0)
    
    # Count the number of even numbers in lst2
    even_count_lst2 = sum(1 for x in lst2 if x % 2 == 0)
    
    # If the number of even numbers in lst2 is greater than or equal to
    # the number of odd numbers in lst1, we can make all elements in lst1 even
    if even_count_lst2 >= odd_count_lst1:
        return "YES"
    else:
        return "NO"

# Example usage:
# print(exchange([1, 2, 3, 4], [1, 2, 3, 4]))  # Output: "YES"
# print(exchange([1, 2, 3, 4], [1, 5, 3, 4]))  # Output: "NO"