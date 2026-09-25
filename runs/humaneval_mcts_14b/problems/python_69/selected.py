def search(lst):
    from collections import Counter
    
    # Step 1: Create a dictionary to count the frequency of each integer in the list
    frequency = Counter(lst)
    
    # Step 2: Initialize a variable to keep track of the greatest valid integer
    greatest_valid_integer = -1
    
    # Step 3: Iterate through the frequency dictionary
    for num, freq in frequency.items():
        # Check if the frequency is greater than or equal to the integer itself
        if freq >= num:
            # Update the greatest valid integer if the current number is greater
            greatest_valid_integer = max(greatest_valid_integer, num)
    
    return greatest_valid_integer

# Test cases
print(search([4, 1, 2, 2, 3, 1]))  # Output: 2
print(search([1, 2, 2, 3, 3, 3, 4, 4, 4]))  # Output: 3
print(search([5, 5, 4, 4, 4]))  # Output: -1