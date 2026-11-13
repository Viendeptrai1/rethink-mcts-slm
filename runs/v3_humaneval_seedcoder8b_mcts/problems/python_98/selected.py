def count_upper(s):
    return len([c for i, c in enumerate(s) if i % 2 == 0 and c.isupper() and c in 'AEIOU'])