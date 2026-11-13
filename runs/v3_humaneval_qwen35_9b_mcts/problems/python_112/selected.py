def reverse_delete(s, c):
    result_chars = []
    for char in s:
        if char not in c:
            result_chars.append(char)
    result_string = ''.join(result_chars)
    is_palindrome = result_string == result_string[::-1]
    return (result_string, is_palindrome)