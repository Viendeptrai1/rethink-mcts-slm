def count_upper(s: str) -> int:
    """
    Given a string s, count the number of uppercase vowels in even indices.
    
    Uppercase vowels: A, E, I, O, U
    Even indices: 0, 2, 4, ...
    """
    count = 0
    vowels = set('AEIOU')
    
    for i, char in enumerate(s):
        if i % 2 == 0 and char in vowels:
            count += 1
            
    return count