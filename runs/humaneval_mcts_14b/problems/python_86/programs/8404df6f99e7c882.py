def anti_shuffle(s):
    import re
    
    # Split the string into words and spaces
    words = re.findall(r'\S+|\s+', s)
    
    # Sort characters in each word
    sorted_words = [''.join(sorted(word)) for word in words]
    
    # Join the sorted words back together
    return ''.join(sorted_words)

# Example usage:
# print(anti_shuffle('Hi'))  # Output: 'Hi'
# print(anti_shuffle('hello'))  # Output: 'ehllo'
# print(anti_shuffle('Hello World!!!'))  # Output: 'Hello !!!Wdlor'