def evaluate_expression(expression):
    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '*':
            values.append(left * right)

    def precedence(op):
        if op == '+':
            return 1
        if op == '*':
            return 2
        return 0

    def evaluate(tokens):
        values = []
        operators = []
        i = 0
        while i < len(tokens):
            if tokens[i] == ' ':
                i += 1
                continue
            if tokens[i] == '(':
                operators.append(tokens[i])
            elif tokens[i].isdigit():
                val = 0
                while i < len(tokens) and tokens[i].isdigit():
                    val = (val * 10) + int(tokens[i])
                    i += 1
                values.append(val)
                i -= 1
            elif tokens[i] == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()
            else:
                while (operators and precedence(operators[-1]) >= precedence(tokens[i])):
                    apply_operator(operators, values)
                operators.append(tokens[i])
            i += 1

        while operators:
            apply_operator(operators, values)

        return values[0]

    return evaluate(expression)

def maximize_expression(s):
    max_value = float('-inf')
    n = len(s)

    for i in range(1, n, 2):
        for j in range(i + 2, n + 1, 2):
            expression = list(s)
            expression.insert(j, ')')
            expression.insert(i, '(')
            value = evaluate_expression(''.join(expression))
            max_value = max(max_value, value)

    return max_value

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = maximize_expression(input)
    print(result)