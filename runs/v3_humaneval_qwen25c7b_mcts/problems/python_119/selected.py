def match_parens(lst):
    def is_balanced(s):
        balance = 0
        for char in s:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    first_order = lst[0] + lst[1]
    second_order = lst[1] + lst[0]

    return 'Yes' if is_balanced(first_order) or is_balanced(second_order) else 'No'