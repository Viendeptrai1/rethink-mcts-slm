def max_expression_value(s):
    def evaluate(expression):
        stack = []
        i = 0
        while i < len(expression):
            if expression[i].isdigit():
                num = int(expression[i])
                i += 1
                while i < len(expression) and expression[i].isdigit():
                    num = num * 10 + int(expression[i])
                    i += 1
                stack.append(num)
            elif expression[i] == '+':
                i += 1
                num = int(expression[i])
                i += 1
                while i < len(expression) and expression[i].isdigit():
                    num = num * 10 + int(expression[i])
                    i += 1
                stack.append(num)
            elif expression[i] == '*':
                i += 1
                num = int(expression[i])
                i += 1
                while i < len(expression) and expression[i].isdigit():
                    num = num * 10 + int(expression[i])
                    i += 1
                stack[-1] *= num
        return sum(stack)

    max_value = float('-inf')
    for i in range(1, len(s) - 1, 2):
        left = evaluate(s[:i])
        right = evaluate(s[i+1:])
        if s[i] == '+':
            total = left + right
        else:
            total = left * right
        max_value = max(max_value, total)

    return max_value

# Read input
import sys
input = sys.stdin.read().strip()

# Output the result
print(max_expression_value(input))