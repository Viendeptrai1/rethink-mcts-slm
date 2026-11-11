def is_bored(S):
    # Split the string into sentences using '.', '?', and '!' as delimiters
    import re
    sentences = re.split(r'[.?!]', S)
    
    # Count the number of sentences that start with "I"
    boredom_count = sum(1 for sentence in sentences if sentence.strip().startswith("I"))
    
    return boredom_count