def pluck(arr):
    # Initialize variables to store the smallest even value and its index
    smallest_even_value = float('inf')
    smallest_index = -1
    
    # Iterate through the array to find the smallest even value and its index
    for index, value in enumerate(arr):
        if value % 2 == 0:  # Check if the value is even
            if value < smallest_even_value:
                smallest_even_value = value
                smallest_index = index
    
    # If no even value was found, return an empty list
    if smallest_index == -1:
        return []
    
    # Return the smallest even value and its index as a list
    return [smallest_even_value, smallest_index]