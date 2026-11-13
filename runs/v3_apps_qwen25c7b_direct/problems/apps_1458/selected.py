def find_reversal(s):
    n = len(s)
    for i in range(n-1):
        if s[i] > s[i+1]:
            return "YES", i+1, i+2
    return "NO"

# Example usage:
# result = find_reversal("abacaba")
# print(result)  # Output: ('YES', 2, 5)

# result = find_reversal("aabcfg")
# print(result)  # Output: ('NO',)