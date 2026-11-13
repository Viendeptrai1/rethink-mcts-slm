def replace_question_marks(n, s):
    stack = []
    result = list(s)
    
    for i in range(n):
        if s[i] == '(' or s[i] == ')':
            stack.append(s[i])
        elif s[i] == '?':
            if len(stack) > 0 and stack[-1] == '(':
                result[i] = ')'
                stack.pop()
            else:
                result[i] = '('
                stack.append('(')
    
    # Check if the final sequence is a correct parenthesis sequence
    if len(stack) != 0:
        return ':('
    
    # Ensure no strict prefix is a correct parenthesis sequence
    for i in range(1, n):
        if result[:i].count('(') == result[:i].count(')'):
            return ':('
    
    return ''.join(result)

# Example usage:
n = int(input().strip())
s = input().strip()
print(replace_question_marks(n, s))