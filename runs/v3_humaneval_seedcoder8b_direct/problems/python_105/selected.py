def by_length(arr):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    
    filtered = [x for x in arr if x in numbers]
    sorted_reversed = sorted(filtered, reverse=True)
    
    return [names[num-1] for num in sorted_reversed]