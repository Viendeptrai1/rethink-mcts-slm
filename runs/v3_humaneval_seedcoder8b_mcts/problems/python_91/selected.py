def is_bored(S):
    import re
    sentences = re.split(r'[.?!]', S)
    boredom_count = 0
    for sentence in sentences:
        stripped_sentence = sentence.strip()
        if stripped_sentence.startswith("I"):
            boredom_count += 1
    return boredom_count