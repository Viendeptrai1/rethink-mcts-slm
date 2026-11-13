def solution(lst):
    total = 0
    for index, value in enumerate(lst):
        if index % 2 == 0 and value % 2 == 1:
            total += value
    return total