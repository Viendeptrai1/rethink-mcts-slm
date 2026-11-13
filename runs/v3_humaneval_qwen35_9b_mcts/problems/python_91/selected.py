def is_bored(S):
    """
    You'll be given a string of words, and your task is to count the number
    of boredoms. A boredom is a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.
   
    For example:
    >>> is_bored("Hello world")
    0
    >>> is_bored("The sky is blue. The sun is shining. I love this weather")
    1
    """
    if not S:
        return 0

    count = 0
    i = 0
    n = len(S)
    
    while i < n:
        # Skip leading whitespace
        while i < n and S[i] in ' \t\n\r':
            i += 1
        
        if i >= n:
            break
        
        # Check if the first word is "I"
        # We need to read the first word character by character
        word_start = i
        while i < n and S[i] not in ' .?!':
            i += 1
        
        # Extract the first word
        first_word = S[word_start:i]
        
        # Check if it is exactly "I" (case-sensitive as per typical problem constraints unless specified otherwise)
        if first_word == "I":
            count += 1
        
        # Move past the delimiter if present
        if i < n and S[i] in '.?!':
            i += 1
    
    return count