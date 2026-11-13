def by_length(arr):
    number_to_name = {
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
    
    filtered_sorted = sorted([x for x in arr if 1 <= x <= 9], reverse=True)
    return [number_to_name[x] for x in filtered_sorted]