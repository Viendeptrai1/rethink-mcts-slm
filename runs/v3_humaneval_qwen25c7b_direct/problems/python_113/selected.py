def odd_count(lst):
    result = []
    for s in lst:
        num_odds = sum(1 for char in s if int(char) % 2 != 0)
        result.append(f"the number of odd elements {num_odds}n the str{num_odds}ng {num_odds} of the {num_odds}nput.")
    return result