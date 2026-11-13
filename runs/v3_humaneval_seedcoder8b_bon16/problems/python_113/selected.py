def odd_count(lst):
    result = []
    for string in lst:
        odd_count = sum(1 for char in string if int(char) % 2 != 0)
        result.append(f"the number of odd elements {odd_count}n the str{odd_count}ng {odd_count} of the {odd_count}nput.")
    return result