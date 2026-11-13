def match_parens(lst):
    def is_balanced(s):
        count = 0
        for char in s:
            if char == '(':
                count += 1
            else:
                count -= 1
            if count < 0:
                return False
        return count == 0

    s1, s2 = lst
    return 'Yes' if is_balanced(s1 + s2) or is_balanced(s2 + s1) else 'No'