from collections import Counter

def search(lst):
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