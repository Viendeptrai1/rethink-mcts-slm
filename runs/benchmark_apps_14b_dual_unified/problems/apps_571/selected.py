def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    
    balance = 0
    result = []
    question_marks = []
    
    for i, char in enumerate(s):
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        else:
            question_marks.append(i)
        
        if balance < 0:
            return ":("
        
        result.append(char)
    
    if balance != 0:
        return ":("
    
    for i in question_marks:
        if balance > 0:
            result[i] = ')'
            balance -= 1
        else:
            result[i] = '('
            balance += 1
    
    return ''.join(result)

if __name__ == "__main__":
    print(solve())