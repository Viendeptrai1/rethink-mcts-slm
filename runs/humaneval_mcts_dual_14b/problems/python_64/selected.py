def vowels_count(s):
    vowels = set('aeiouAEIOU')
    count = sum(1 for char in s if char in vowels)
    
    # Check if 'y' or 'Y' is at the end of the string
    if s.endswith('y') or s.endswith('Y'):
        count += 1
    
    return count

# Test cases
print(vowels_count("abcde"))  # Expected output: 2
print(vowels_count("ACEDY"))  # Expected output: 3
print(vowels_count(""))       # Expected output: 0
print(vowels_count("bcdfg"))  # Expected output: 0
print(vowels_count("rhythm")) # Expected output: 0
print(vowels_count("happy"))  # Expected output: 2
print(vowels_count("Y"))      # Expected output: 1
print(vowels_count("AEIOUY")) # Expected output: 6