def by_length(arr):
    num_to_word = {
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
    filtered_sorted_nums = sorted([num for num in arr if 1 <= num <= 9])
    reversed_nums = filtered_sorted_nums[::-1]
    return [num_to_word[num] for num in reversed_nums]