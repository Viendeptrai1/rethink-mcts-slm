import re

def anti_shuffle(s):
    def sort_word(word):
        return ''.join(sorted(word))
    
    # Split the string into words and non-word characters
    parts = re.findall(r'\w+|\W+', s)
    
    # Sort each word while keeping non-word characters unchanged
    sorted_parts = [sort_word(part) if part.isalpha() else part for part in parts]
    
    # Join the parts back together
    return ''.join(sorted_parts)

# Example usage:
# print(anti_shuffle('Hello World!!!'))  # Output: 'Hello !!!Wdlor'