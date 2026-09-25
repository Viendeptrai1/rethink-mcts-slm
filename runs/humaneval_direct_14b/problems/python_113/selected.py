def odd_count(lst):
    result = []
    for s in lst:
        odd_count = sum(1 for char in s if int(char) % 2 != 0)
        template = "the number of odd elements {}n the str{}ng {} of the {}nput."
        result.append(template.format(odd_count, odd_count, odd_count, odd_count))
    return result