def reverse_delete(s, c):
    filtered_s = ''.join(char for char in s if char not in c)
    reversed_s = filtered_s[::-1]
    is_palindrome = filtered_s == reversed_s
    return (filtered_s, is_palindrome)