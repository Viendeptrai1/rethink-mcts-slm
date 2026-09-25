def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
    # Step 1: Convert the entire string to lowercase to ensure case insensitivity.
    lower_string = string.lower()
    
    # Step 2: Use a set to find distinct characters.
    distinct_characters = set(lower_string)
    
    # Step 3: Return the number of distinct characters.
    return len(distinct_characters)