def sum_squares(lst):
    total = 0
    for index, value in enumerate(lst):
        if index % 3 == 0:
            total += value ** 2
        elif index % 4 == 0:
            total += value ** 3
        else:
            total += value
    return total