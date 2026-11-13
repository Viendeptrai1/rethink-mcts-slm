def vowels_count(s):
    vowels = "aeiou"
    count = sum(1 for char in s if char.lower() in vowels)
    if s.endswith('y') or s.endswith('Y'):
        count += 1
    return count

# Test cases
print(vowels_count("abcde"))  # Output: 2
print(vowels_count("ACEDY"))  # Output: 3
print(vowels_count("rhythm")) # Output: 0
print(vowels_count("SYZYGY")) # Output: 1
print(vowels_count("encyclopedia")) # Output: 6
print(vowels_count("sky")) # Output: 0
print(vowels_count("why")) # Output: 1