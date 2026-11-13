import sys

def solve():
    try:
        input_data = sys.stdin.read().splitlines()
        if not input_data:
            return
        
        # First line is length, second line is the program
        try:
            length = int(input_data[0].strip())
            program = input_data[1]
        except (IndexError, ValueError):
            return

        # Mapping of opening to closing delimiters
        pairs = {
            '(': ')',
            '[': ']',
            '{': '}'
        }
        
        # Stack to keep track of opening delimiters
        stack = []
        
        # Iterate through each character in the program
        for i, char in enumerate(program):
            if char in pairs:
                # It's an opening delimiter, push to stack
                stack.append(char)
            elif char in pairs.values():
                # It's a closing delimiter
                if not stack:
                    # No matching opening delimiter
                    print(f"{char} {i}")
                    return
                
                top = stack.pop()
                if pairs[top] != char:
                    # Mismatch found
                    print(f"{char} {i}")
                    return
            # Ignore spaces and other characters (though problem says only those chars and spaces)
        
        # If we reach here, either no error or more opening than closing
        print("ok so far")

if __name__ == "__main__":
    solve()