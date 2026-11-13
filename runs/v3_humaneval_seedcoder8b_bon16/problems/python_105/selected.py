def by_length(arr):
    digit_names = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    
    # Filter, sort, and reverse the array
    filtered = sorted([x for x in arr if 1 <= x <= 9], reverse=True)
    
    # Convert digits to their names
    return [digit_names[num] for num in filtered]