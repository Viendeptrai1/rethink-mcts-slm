import sys

def solve():
    try:
        input_data = sys.stdin.read().splitlines()
        if not input_data:
            return
        
        # Filter out empty lines if any, though problem says two lines
        lines = [line for line in input_data if line.strip() != '']
        if len(lines) < 2:
            return
            
        length = int(lines[0].strip())
        program = lines[1]
        
        # Mapping of closing to opening delimiters
        matching = {')': '(', ']': '[', '}': '{'}
        stack = []
        
        for i, char in enumerate(program):
            if char == ' ':
                continue
            
            if char in '([{':
                stack.append(char)
            elif char in ')]}':
                if not stack:
                    print(f"{char} {i}")
                    return
                top = stack.pop()
                if matching[char] != top:
                    print(f"{char} {i}")
                    return
        
        print("ok so far")
        
    except Exception:
        pass

if __name__ == "__main__":
    solve()