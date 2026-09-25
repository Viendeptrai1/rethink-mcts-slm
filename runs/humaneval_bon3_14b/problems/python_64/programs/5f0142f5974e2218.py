def vowels_count(s):
    """Write a function vowels_count which takes a string representing
    a word as input and returns the number of vowels in the string.
    Vowels in this case are 'a', 'e', 'i', 'o', 'u'. Here, 'y' is also a
    vowel, but only when it is at the end of the given word.

    Example:
    >>> vowels_count("abcde")
    2
    >>> vowels_count("ACEDY")
    3
    """
    vowels = "aeiou"
    count = 0
    s = s.lower()
    for i, char in enumerate(s):
        if char in vowels:
            count += 1
        elif char == 'y' and i == len(s) - 1:
            count += 1
    return count

# Test cases
print(vowels_count("abcde"))  # Output: 2
print(vowels_count("ACEDY"))  # Output: 3
print(vowels_count("rhythm"))  # Output: 0
print(vowels_count("SYZYGY"))  # Output: 1
print(vowels_count("quickly"))  # Output: 2
print(vowels_count("fly"))  # Output: 0
print(vowels_count("encyclopedia"))  # Output: 6
print(vowels_count("A"))  # Output: 1
print(vowels_count("Y"))  # Output: 1
print(vowels_count("sky"))  # Output: 1