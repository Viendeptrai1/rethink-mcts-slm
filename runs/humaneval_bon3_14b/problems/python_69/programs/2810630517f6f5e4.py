def search(lst):
    from collections import Counter
    
    # Count the frequency of each integer in the list
    frequency = Counter(lst)
    
    # Initialize the result as -1 (in case no valid integer is found)
    result = -1
    
    # Iterate over the frequency dictionary
    for num, freq in frequency.items():
        # Check if the frequency is greater than or equal to the integer itself
        if freq >= num:
            # Update the result with the maximum valid integer found
            result = max(result, num)
    
    return result

# Test cases
print(search([4, 1, 2, 2, 3, 1]))  # Output: 2
print(search([1, 2, 2, 3, 3, 3, 4, 4, 4]))  # Output: 3
print(search([5, 5, 4, 4, 4]))  # Output: -1