def replace_question_marks(s):
    n = len(s)
    stack = []
    result = list(s)
    
    for i in range(n):
        if s[i] == '(' or s[i] == '?':
            stack.append(i)
        elif s[i] == ')':
            if stack:
                stack.pop()
            else:
                return ":(("
    
    if stack:
        for j in stack:
            if j > 0 and result[j-1] != '(':
                result[j] = '('
            else:
                result[j] = ')'
    
    return ''.join(result)

# Example usage:
# print(replace_question_marks("(?????"))
# print(replace_question_marks("(???(???(?"))