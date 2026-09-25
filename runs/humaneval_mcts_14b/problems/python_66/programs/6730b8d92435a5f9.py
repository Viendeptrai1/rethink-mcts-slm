def digitSum(s):
    total = 0
    for char in s:
        if char.isupper():
            total += ord(char)
    return total

# Test cases
print(digitSum(""))          # Output: 0
print(digitSum("abAB"))      # Output: 131
print(digitSum("abcCd"))     # Output: 67
print(digitSum("helloE"))    # Output: 69
print(digitSum("woArBld"))   # Output: 131
print(digitSum("aAaaaXa"))   # Output: 153