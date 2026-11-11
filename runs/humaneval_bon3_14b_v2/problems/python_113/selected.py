def odd_count(lst):
    def count_odds(s):
        return sum(1 for char in s if int(char) % 2 == 1)
    
    result = []
    for i, s in enumerate(lst):
        odd_count = count_odds(s)
        template = "the number of odd elements {}n the str{}ng {} of the {}nput."
        result.append(template.format(odd_count, odd_count, odd_count, odd_count))
    
    return result