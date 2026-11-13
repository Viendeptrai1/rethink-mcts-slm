def replace_question_marks(n, s):
    stack = []
    result = list(s)
    
    for i in range(n):
        if s[i] == '(':
            stack.append(i)
        elif s[i] == ')':
            if stack:
                stack.pop()
            else:
                return ':('
        elif s[i] == '?':
            if stack:
                result[i] = '('
                stack.pop()
            else:
                result[i] = ')'
    
    if stack:
        return ':('

    open_brackets = result.count('(')
    close_brackets = result.count(')')
    
    if open_brackets != close_brackets:
        return ':('

    for i in range(n-1, -1, -1):
        if result[i] == '?':
            result[i] = ')' if i % 2 == 0 else '('

    return ''.join(result)


# Example usage:
n = int(input().strip())
s = input().strip()
print(replace_question_marks(n, s))