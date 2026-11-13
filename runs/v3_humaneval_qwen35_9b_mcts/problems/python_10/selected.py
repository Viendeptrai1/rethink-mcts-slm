def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
    if not string:
        return string

    n = len(string)
    # dp[i][j] will be True if string[i:j+1] is a palindrome
    dp = [[False] * n for _ in range(n)]

    # Every single character is a palindrome
    for i in range(n):
        dp[i][i] = True

    # Check for palindromes of length 2
    for i in range(n - 1):
        if string[i] == string[i + 1]:
            dp[i][i + 1] = True

    # Check for palindromes of length > 2
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if string[i] == string[j] and dp[i + 1][j - 1]:
                dp[i][j] = True

    # Find the longest palindromic suffix
    # We want the largest length such that string[n-length:n] is a palindrome
    longest_pal_suffix_len = 0
    for length in range(n, 0, -1):
        start_index = n - length
        if dp[start_index][n - 1]:
            longest_pal_suffix_len = length
            break

    # The part before the palindromic suffix needs to be reversed and appended
    prefix_to_reverse = string[:n - longest_pal_suffix_len]
    return string + prefix_to_reverse[::-1]