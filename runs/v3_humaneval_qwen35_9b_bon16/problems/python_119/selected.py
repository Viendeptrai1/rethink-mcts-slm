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

    s1 = lst[0]
    s2 = lst[1]

    if is_balanced(s1 + s2):
        return 'Yes'
    if is_balanced(s2 + s1):
        return 'Yes'
    return 'No'