def odd_count(lst):
    def count_odds(s):
        return sum(1 for char in s if int(char) % 2 != 0)
    
    return [f"the number of odd elements {count_odds(s)}n the str{count_odds(s)}ng {count_odds(s)} of the {count_odds(s)}nput." for s in lst]