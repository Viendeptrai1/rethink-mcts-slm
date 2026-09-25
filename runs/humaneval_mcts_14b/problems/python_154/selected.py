def cycpattern_check(a, b):
    """You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word
    cycpattern_check("abcd","abd") => False
    cycpattern_check("hello","ell") => True
    cycpattern_check("whassup","psus") => False
    cycpattern_check("abab","baa") => True
    cycpattern_check("efef","eeff") => False
    cycpattern_check("himenss","simen") => True
    """
    # Step 1: Check if the second word is a substring of the first word
    if b in a:
        return True
    
    # Step 2: Generate all rotations of the second word
    for i in range(len(b)):
        rotated_b = b[i:] + b[:i]
        # Step 3: Check if the current rotation is a substring of the first word
        if rotated_b in a:
            return True
    
    # If no rotation is a substring, return False
    return False