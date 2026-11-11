def is_bored(S):
    import re
    # Split the string into sentences using regex to match '.', '?', or '!'
    sentences = re.split(r'[.?!]', S)
    # Initialize a counter for boredoms
    boredom_count = 0
    # Iterate through each sentence
    for sentence in sentences:
        # Strip leading and trailing whitespace and check if it starts with 'I'
        if sentence.strip().startswith('I'):
            boredom_count += 1
    return boredom_count