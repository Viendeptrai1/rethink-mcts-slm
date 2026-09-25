def by_length(arr):
    # Define a mapping from digits to their corresponding names
    digit_to_name = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine"
    }
    
    # Filter the array to include only numbers between 1 and 9 inclusive
    filtered_arr = [num for num in arr if 1 <= num <= 9]
    
    # Sort the filtered array
    sorted_arr = sorted(filtered_arr)
    
    # Reverse the sorted array
    reversed_arr = sorted_arr[::-1]
    
    # Map each number to its corresponding name
    result = [digit_to_name[num] for num in reversed_arr]
    
    return result