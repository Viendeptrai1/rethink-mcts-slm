import re

def words_string(s):
    # Use regular expression to split the string by commas or spaces
    words = re.split(r'[,\s]+', s)
    # Filter out any empty strings that may result from consecutive delimiters
    return [word for word in words if word]

# Example usage:
# print(words_string("Hi, my name is John"))
# print(words_string("One, two, three, four, five, six"))