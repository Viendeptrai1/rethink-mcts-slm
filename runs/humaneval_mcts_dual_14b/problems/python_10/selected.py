def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]

def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string. """
    if not string:
        return string
    
    # Find the longest palindromic suffix
    for i in range(len(string)):
        if is_palindrome(string[i:]):
            # Append the reverse of the prefix before the palindromic suffix
            return string + string[:i][::-1]
    
    # In case no palindromic suffix is found, which is unlikely due to the loop logic
    return string + string[::-1]