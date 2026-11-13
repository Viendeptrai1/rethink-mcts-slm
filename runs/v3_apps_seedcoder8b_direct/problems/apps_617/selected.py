def max_expression_value(s: str) -> int:
    # Parse the input string into numbers and operators
    numbers = list(map(int, s[::2]))
    operators = s[1::2]
    
    # Initialize the maximum value
    max_value = float('-inf')
    
    # Try placing brackets between every pair of numbers
    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            # Calculate the value of the expression with brackets
            temp_value = calculate_with_brackets(numbers, operators, i, j)
            max_value = max(max_value, temp_value)
    
    return max_value

def calculate_with_brackets(numbers, operators, start, end):
    # Calculate the value of the expression with brackets around numbers[start:end+1]
    # First calculate the sub-expression inside the brackets
    sub_expr_value = numbers[start]
    for k in range(start, end):
        if operators[k] == '+':
            sub_expr_value += numbers[k + 1]
        elif operators[k] == '*':
            sub_expr_value *= numbers[k + 1]
    
    # Now calculate the full expression with the sub-expression inside brackets
    result = numbers[0]
    for k in range(len(operators)):
        if k == start - 1:
            result = sub_expr_value
        elif k < start - 1:
            if operators[k] == '+':
                result += numbers[k + 1]
            elif operators[k] == '*':
                result *= numbers[k + 1]
        else:
            if operators[k] == '+':
                result += numbers[k + 1]
            elif operators[k] == '*':
                result *= numbers[k + 1]
    
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(max_expression_value(input))